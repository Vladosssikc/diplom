import allure
import pytest
from pages.MainPage import MainPage
from pages.CartPage import CartPage


@allure.epic("Читай-город")
@allure.suite('UI')
@allure.severity(severity_level='high')
@allure.title('Поиск товара по ключевым словам')
@allure.description('Проверка корректности работы функции поиска товаров на сайте с различными входными данными.')
@allure.feature('Test 1')
@pytest.mark.parametrize('input', [
    'Test',
    'Дюна',
    '123',
    ',,'
])
def test_positive_search(browser, config, input: str):
    search = MainPage(browser, config)

    @allure.step("Переходим на главную страницу")
    def go_to_main_page():
        search.go_to_page()

    @allure.step("Выполняем поиск с входными данными: {input}")
    def perform_search(input):
        search.search(input)

    @allure.step("Получаем текущий URL")
    def get_url():
        return search.get_current_url()

    @allure.step("Проверяем, что поисковая строка принимает вводные данные")
    def check_search_result(url):
        assert '/search?phrase=' in url

    go_to_main_page()
    perform_search(input)
    current_url = get_url()
    check_search_result(current_url)


@allure.epic("Читай-город")
@allure.suite('UI')
@allure.severity(severity_level='low')
@allure.title('Поиск товара по ключевым словам')
@allure.description('Проверка корректности работы функции поиска товаров на сайте с различными входными данными.')
@allure.feature('Test 2')
@pytest.mark.xfail()
@pytest.mark.parametrize('input', [
    '$%^',
    '',
    ' ',
    None
])
def test_negative_search(browser, config, input: str):
    search = MainPage(browser, config)

    @allure.step("Переходим на главную страницу")
    def go_to_main_page():
        search.go_to_page()

    @allure.step("Выполняем поиск с входными данными: {input}")
    def perform_search(input):
        search.search(input)

    @allure.step("Получаем текущий URL")
    def get_url():
        return search.get_current_url()

    @allure.step("Проверяем, что поисковая строка не принимает вводные данные")
    def check_search_result(url):
        assert '/search?phrase=' in url

    go_to_main_page()
    perform_search(input)
    current_url = get_url()
    check_search_result(current_url)


@allure.epic("Читай-город")
@allure.suite('UI')
@allure.severity(severity_level='high')
@allure.title('Добавление товара в корзину')
@allure.description('Проверка возможности добавления товара в корзину.')
@allure.feature('Test 3')
def test_add_to_cart(browser, config):
    main = MainPage(browser, config)
    cart = CartPage(browser, config)

    @allure.step("Проверяем количество товаров в корзине до добавления")
    def check_cart_before():
        return cart.go_to_cart()

    @allure.step("Переходим на главную страницу")
    def go_to_main_page():
        main.go_to_page()

    @allure.step("Добавляем товар в корзину")
    def add_item_to_cart():
        main.add_to_cart()

    @allure.step("Проверяем количество товаров в корзине после добавления")
    def check_cart_after():
        return cart.go_to_cart()

    @allure.step("Очищаем корзину")
    def clear_cart():
        cart.clear_cart()

    @allure.step("Проверяем, что в корзине стало на один товар больше")
    def check_cart_difference(before, after):
        assert after - before == 1

    items_in_cart_before = check_cart_before()
    go_to_main_page()
    add_item_to_cart()
    items_in_cart_after = check_cart_after()
    clear_cart()
    check_cart_difference(items_in_cart_before, items_in_cart_after)


@allure.epic("Читай-город")
@allure.suite('UI')
@allure.severity(severity_level='high')
@allure.title('Оформление заказа')
@allure.description('Проверка возможности оформления заказа со стандартными данными пользователя.')
@allure.feature('Test 4')
def test_default_user_order(browser, config):
    main = MainPage(browser, config)
    cart = CartPage(browser, config)

    @allure.step("Переходим на главную страницу")
    def go_to_main_page():
        main.go_to_page()

    @allure.step("Добавляем товар в корзину")
    def add_item_to_cart():
        main.add_to_cart()

    @allure.step("Переходим в корзину")
    def go_to_cart():
        cart.go_to_cart()

    @allure.step("Переходим на страницу оформления заказа")
    def go_to_order_page():
        cart.go_to_order_page()

    @allure.step("Выбираем город в России")
    def choose_city():
        cart.choose_city_in_rus()

    @allure.step("Выбираем пункт выдачи")
    def choose_pickup():
        cart.choose_pickup_point()

    @allure.step("Оформляем заказ")
    def checkout():
        return cart.checkout_order()

    @allure.step("Отменяем заказ")
    def cancel_order():
        main.cancel_orders()

    @allure.step("Очищаем корзину")
    def clear_cart():
        cart.clear_cart()

    @allure.step("Проверяем успешное оформление заказа")
    def check_order_success(success):
        assert success is True

    go_to_main_page()
    add_item_to_cart()
    go_to_cart()
    go_to_order_page()
    choose_city()
    choose_pickup()
    success = checkout()
    if success:
        cancel_order()
    else:
        clear_cart()
    check_order_success(success)


@allure.epic("Читай-город")
@allure.suite('UI')
@allure.severity(allure.severity_level.NORMAL)
@allure.title('Проверка различных методов оплаты')
@allure.description('Проверка оформления заказа разными методами оплаты.')
@allure.feature('Test 5')
@pytest.mark.parametrize('payment_method', [
    'sbp',
    'webcard',
    'face-to-face'
])
def test_payment_methods(browser, config, payment_method: str):
    main = MainPage(browser, config)
    cart = CartPage(browser, config)

    @allure.step("Переходим на главную страницу")
    def go_to_main_page():
        main.go_to_page()

    @allure.step("Добавляем товар в корзину")
    def add_item_to_cart():
        main.add_to_cart()

    @allure.step("Переходим в корзину")
    def go_to_cart():
        cart.go_to_cart()

    @allure.step("Переходим на страницу оформления заказа")
    def go_to_order_page():
        cart.go_to_order_page()

    @allure.step("Выбираем город в России")
    def choose_city():
        cart.choose_city_in_rus()

    @allure.step("Выбираем пункт выдачи")
    def choose_pickup():
        cart.choose_pickup_point()

    @allure.step("Выбираем метод оплаты: {payment_method}")
    def choose_payment(payment_method):
        cart.choose_payment_method(payment_method)

    @allure.step("Оформляем заказ")
    def checkout():
        return cart.checkout_order()

    @allure.step("Отменяем заказ")
    def cancel_order():
        main.cancel_orders()

    @allure.step("Очищаем корзину")
    def clear_cart():
        cart.clear_cart()

    @allure.step("Проверяем успешное оформление заказа")
    def check_order_success(success):
        assert success is True

    go_to_main_page()
    add_item_to_cart()
    go_to_cart()
    go_to_order_page()
    choose_city()
    choose_pickup()
    choose_payment(payment_method)
    success = checkout()
    if success:
        cancel_order()
    else:
        clear_cart()
    check_order_success(success)
