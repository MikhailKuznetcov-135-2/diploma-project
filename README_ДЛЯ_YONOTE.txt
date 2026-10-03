ТЕСТИРОВАНИЕ ПЛАТФОРМЫ YOUGILE — ДИПЛОМНЫЙ ПРОЕКТ

Цель работы

Проверить ключевой пользовательский путь YouGile: авторизацию, проекты,
доски, колонки и задачи, а также публичный REST API v2. Подготовить ручную
документацию, API-коллекцию и автотесты с воспроизводимым отчётом.

Что выполнено

- 7 функциональных сценариев: 7 PASSED;
- 7 API-сценариев: 7 PASSED;
- 12 автотестов pytest: 12 PASSED;
- Newman: 15 assertions, 0 failures;
- UI-прогон в Chromium, Firefox и WebKit: 5/5 PASSED в каждом браузере;
- 12 нефункциональных проверок: 10 PASSED, 2 FAILED;
- подтверждён и оформлен один дефект YG-DIP-001.

Основной результат

Запланированный объём выполнен полностью. Функциональные сценарии и API
работают в проверенном объёме. Найден дефект клавиатурной навигации: кнопка
«Войти» пропускается при переходе клавишей Tab. Severity — Minor,
Priority — Medium, воспроизводимость — 3/3. Вход по Enter работает.

Отдельно зафиксировано наблюдение по производительности: две из трёх загрузок
страницы входа превысили критерий 3 секунды; среднее время составило 3.387 с.

Стек

Python 3.12, pytest, Requests, Playwright, Allure, Newman и Ruff.
Применён Page Object. Секреты вынесены из кода, временный API-ключ после
прогона удаляется. Комплект не содержит config.yaml и учётных данных.

Вложения к странице

1. test_plan.txt
2. yougile_test_documentation.xlsx
3. yougile_bug_reports.xlsx
4. yougile_postman_collection.json
5. yougile-autotests.zip
6. allure-report.zip
7. evidence.zip
8. yougile_presentation.pptx
9. yougile_video_presentation.mp4
10. СЦЕНАРИЙ_ВИДЕО.txt
11. final_report.txt

Как воспроизвести автопрогон

1. Распаковать yougile-autotests.zip.
2. Создать виртуальное окружение и установить requirements.txt.
3. Выполнить playwright install.
4. Скопировать config.example.yaml в config.yaml и указать свои данные.
5. Запустить pytest --alluredir=allure-results.
6. Открыть отчёт командой allure serve allure-results.

Границы работы

Мобильные приложения, разные роли, сторонние интеграции и нагрузочное
тестирование не входили в согласованный объём диплома.
