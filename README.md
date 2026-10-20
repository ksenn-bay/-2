# Автозамер скорости gosuslugi.ru (лаба 2)

## Настройка (один раз, ~10 минут)
1. Зарегистрируйтесь на github.com (если нет аккаунта).
2. Нажмите + → New repository. Имя любое, например `lab2-speed`. Поставьте Public. Create.
3. На странице репозитория: Add file → Upload files. Перетащите сюда файлы
   `measure.py` и `README.md`. Commit changes.
4. Папку `.github/workflows` через загрузку не добавить, поэтому:
   Add file → Create new file. В поле имени введите ровно
   `.github/workflows/measure.yml`, вставьте туда содержимое файла measure.yml. Commit.
5. (Рекомендуется) Ключ API, чтобы Google не ограничивал запросы:
   console.cloud.google.com → создать проект → «API и сервисы» → включить
   PageSpeed Insights API → «Учётные данные» → создать API-ключ.
   В репозитории: Settings → Secrets and variables → Actions → New repository secret,
   имя `PSI_API_KEY`, значение — ваш ключ.
6. Проверка: вкладка Actions → measure-gosuslugi → Run workflow.
   Через 1–2 минуты в репозитории появится `results.csv` со строкой замера.
   (Этот пробный замер потом можно оставить как День 1.)

## Дальше
Каждый день в 09:00 по Москве добавляется строка. После 10 строк скрипт останавливается.
GitHub может запускать cron с опозданием на 5–30 минут, это нормально, время замера
записывается в таблицу, и его можно указать в отчёте.
Через 10 дней скачайте results.csv и пришлите мне.
