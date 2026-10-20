import csv, json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta

URL = "https://www.gosuslugi.ru/"
STRATEGY = "mobile"          # можно поменять на "desktop"
CSV_FILE = "results.csv"
MAX_DAYS = 10
API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
FIELDS = ["date", "time_msk", "LCP_s", "CLS", "FCP_s", "TTFB_ms", "perf_score"]

def rows():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def fetch():
    params = {"url": URL, "strategy": STRATEGY, "category": "performance", "locale": "ru"}
    key = os.environ.get("PSI_API_KEY")
    if key:
        params["key"] = key
    full = API + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(full, timeout=120) as r:
                return json.load(r)
        except Exception as e:
            last = e
            time.sleep(20 * (attempt + 1))
    raise SystemExit(f"PageSpeed API недоступен: {last}")

def main():
    data = rows()
    if len(data) >= MAX_DAYS:
        print("Уже собрано 10 замеров, ничего не делаю.")
        return
    msk = datetime.now(timezone(timedelta(hours=3)))
    today = msk.strftime("%Y-%m-%d")
    if any(r["date"] == today for r in data) and "--force" not in sys.argv:
        print("Сегодня замер уже есть.")
        return
    res = fetch()["lighthouseResult"]
    a = res["audits"]
    row = {
        "date": today,
        "time_msk": msk.strftime("%H:%M"),
        "LCP_s": round(a["largest-contentful-paint"]["numericValue"] / 1000, 2),
        "CLS": round(a["cumulative-layout-shift"]["numericValue"], 3),
        "FCP_s": round(a["first-contentful-paint"]["numericValue"] / 1000, 2),
        "TTFB_ms": round(a["server-response-time"]["numericValue"]),
        "perf_score": round(res["categories"]["performance"]["score"] * 100),
    }
    new = not os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    print(row)

if __name__ == "__main__":
    main()
