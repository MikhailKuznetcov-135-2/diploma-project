# YouGile diploma autotests

Проверенный проект автотестов веб-версии YouGile и REST API v2.

## Состав

- `api/` — 7 API-тестов;
- `ui/` — 5 UI-тестов с Page Object;
- `conftest.py` — фикстуры браузера и временного API-ключа;
- `config.example.yaml` — безопасный пример конфигурации.

Фактический прогон 03.10.2026: 12/12 тестов PASSED. UI-набор также отдельно
прошёл в Chromium, Firefox и WebKit. Временный API-ключ удаляется после сессии.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
cp config.example.yaml config.yaml
pytest --alluredir=allure-results
allure serve allure-results
```

В `config.yaml` указываются собственные логин и пароль. Этот файл добавлен в
`.gitignore` и намеренно не включён в архив.

Отдельные наборы:

```bash
pytest -m api
pytest -m ui
YOUGILE_BROWSER=firefox pytest -m ui
YOUGILE_BROWSER=webkit pytest -m ui
```

