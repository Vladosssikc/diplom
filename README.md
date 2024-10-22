# Диплом
Дипломная работа. Архитектура фреймворка для сайта "Читай-город"
## Задача проекта

Автоматизация тестирования основного функционала сайта Читай-город:

- авторизация 
- поиск товара
- покупка товара

## Структура проекта

- ./test - тесты
- ./api - работа с API
- ./ui - работа с ui

## Шаги

1. Склонировать проект 'git clone https://github.com/Pobutka/DIPLOM.git'
2. Установить все зависимости из requirements.txt
3. Скопировать access-token по инструкции ниже.
3. Запустить тесты 'pytest -s -v --alluredir=allure-result' ИЛИ 'python -m pytest -s -v --alluredir=allure-result'
4. Сгенерировать отчет 'allure generate allure-files -o allure-report' ИЛИ 'allure serve allure-result '
5. Открыть отчет 'allure open allure-report'

## Инструкция по использованию access-token в проекте

Access-token - это процесс проверки учётных данных пользователя (логин/пароль). Она хранится в файле conf.ini, корневая директория.

### Шаги присвоения access-token

1. Перейти на [сайт](https://www.chitai-gorod.ru/).
2. Авторизироваться.
3. Открыть Панель разработчика.
4. Перейти на вкладку Network и выбрать Fetch/XHR.
5. Перезагрузить главную страницу с открытой панелью.
6. Открыть любой запрос, содержащий в Request Headers строку Authorization.
 Чтобы это проверить:
- Открыть любой запрос с оранжевой иконкой на вкладке Headers.
- Пролистать вниз до Request Headers.
7. Найти в Request Headers строку Authorization и скопировать ее значение без Bearer. 
 *Если в запросе нет такой строки, то попробуйте открыть другие запросы.
8. Открыть файл conf.ini и вставить скопированные данные в переменную access-token без кавычек.
 *Ключ протухает, поэтому иногда нужно менять значение в переменной (примерно каждый час). 

### Стек

- selenium
- requests
- pytest
- allure
- webdriver
- webdriver-manager
- configparser

### Библиотеки (**!**)

- pip install pytest
- pip install selenium
- pip install requests
- pip install allure-pytest
- pip install webdriver-manager
- pip install configparser

