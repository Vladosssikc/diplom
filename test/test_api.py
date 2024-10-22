import allure
import pytest
from API.test_api_logic.Cart import Cart
from API.test_api_logic.Order import Order


@allure.epic("Читай-город")
@allure.suite('API')
@allure.severity(severity_level='critical')
@allure.title('Самовывоз из магазина')
@allure.description('Оформление заказа самовывозом из магазина и его отмена')
@allure.feature('Test 1')
def test_pickup_from_shop(config):
    cart = Cart(config)
    order = Order(config)

    @allure.step("Добавляем товар в корзину")
    def add_to_cart():
        cart.add_to_cart()
        assert cart.view_cart() == int(config.get('data', 'productID'))

    @allure.step("Оформляем заказ")
    def create_order():
        return order.order_create(213, 'shop', 'Ивано Ива ИВ', '79996960530', 
                                  'email@gmail.com')

    @allure.step("Проверяем успешное оформление заказа")
    def check_order(order_id):
        assert order.view_order(order_id) == 200

    @allure.step("Проверяем успешное удаление заказа")
    def delete_order(order_id):
        assert order.delete_order(order_id) == 204

    add_to_cart()
    order_id = create_order()
    check_order(order_id)
    delete_order(order_id)


@allure.epic("Читай-город")
@allure.suite('API')
@allure.severity(severity_level='high')
@allure.title('Курьер в России')
@allure.description('Оформление заказа курьером в России и его отмена')
@allure.feature('Test 2')
def test_courier_in_rus(config):
    cart = Cart(config)
    order = Order(config)

    @allure.step("Добавляем товар в корзину")
    def add_to_cart():
        cart.add_to_cart()
        assert cart.view_cart() == int(config.get('data', 'productID'))

    @allure.step("Оформляем заказ")
    def create_order():
        return order.order_create(213, 'courier', 'Ивано Ива ИВ', '79996960530', 
                                  'email@gmail.com')

    @allure.step("Проверяем успешное оформление заказа")
    def check_order(order_id):
        assert order.view_order(order_id) == 200

    @allure.step("Проверяем успешное удаление заказа")
    def delete_order(order_id):
        assert order.delete_order(order_id) == 204

    add_to_cart()
    order_id = create_order()
    check_order(order_id)
    delete_order(order_id)


@allure.epic("Читай-город")
@allure.suite('API')
@allure.severity(severity_level='high')
@allure.title('Почта РФ')
@allure.description('Оформление заказа почтой РФ и его отмена')
@allure.feature('Test 3')
def test_rus_post(config):
    cart = Cart(config)
    order = Order(config)

    @allure.step("Добавляем товар в корзину")
    def add_to_cart():
        cart.add_to_cart()
        assert cart.view_cart() == int(config.get('data', 'productID'))

    @allure.step("Оформляем заказ")
    def create_order():
        return order.order_create(213, 'post', 'Ивано Ива ИВ', '79996960530', 
                                  'email@gmail.com')

    @allure.step("Проверяем успешное оформление заказа")
    def check_order(order_id):
        assert order.view_order(order_id) == 200

    @allure.step("Проверяем успешное удаление заказа")
    def delete_order(order_id):
        assert order.delete_order(order_id) == 204

    add_to_cart()
    order_id = create_order()
    check_order(order_id)
    delete_order(order_id)


@allure.epic("Читай-город")
@allure.suite('API')
@allure.severity(severity_level='low')
@allure.title('Пользователь с английским именем')
@allure.description('Заказ курьером в России от пользователя с английским именем и его отмена')
@allure.feature('Test 4')
def test_courier_latin_username(config):
    cart = Cart(config)
    order = Order(config)

    @allure.step("Добавляем товар в корзину")
    def add_to_cart():
        cart.add_to_cart()
        assert cart.view_cart() == int(config.get('data', 'productID'))

    @allure.step("Оформляем заказ")
    def create_order():
        return order.order_create(213, 'courier', 'Lohn John', '79996960530', 
                                  'email@gmail.com')

    @allure.step("Проверяем неуспешное оформление заказа")
    def check_order(order_id):
        assert order.view_order(order_id) == 400

    add_to_cart()
    order_id = create_order()
    check_order(order_id)


@allure.epic("Читай-город")
@allure.suite('API')
@allure.severity(severity_level='low')
@allure.title('Почта с недействительным доменом')
@allure.description('Оформление заказа самовывозом из магазина от пользователя с почтой с недействительным доменом и его отмена')
@allure.feature('Test 5')
@pytest.mark.xfail()
def test_useremail_with_wrong_domain(config):
    cart = Cart(config)
    order = Order(config)

    @allure.step("Добавляем товар в корзину")
    def add_to_cart():
        cart.add_to_cart()
        assert cart.view_cart() == int(config.get('data', 'productID'))

    @allure.step("Оформляем заказ")
    def create_order():
        return order.order_create(213, 'shop', 'Ивано Ива ИВ', '79996960530', 
                                  'sanich@aaa.aaaaa')

    @allure.step("Проверяем успешное оформление заказа")
    def check_order(order_id):
        res = order.view_order(order_id)
        order.delete_order(order_id)
        assert res == 200

    add_to_cart()
    order_id = create_order()
    check_order(order_id)


@allure.epic("Читай-город")
@allure.suite('API')
@allure.severity(severity_level='low')
@allure.title('Телефон с недействительным кодом страны')
@allure.description('Оформление заказа самовывозом из магазина от пользователя с телефоном с недействительным кодом страны и его отмена')
@allure.feature('Test 6')
@pytest.mark.xfail()
def test_userephone_with_wrong_code(config):
    cart = Cart(config)
    order = Order(config)

    @allure.step("Добавляем товар в корзину")
    def add_to_cart():
        cart.add_to_cart()
        assert cart.view_cart() == int(config.get('data', 'productID'))

    @allure.step("Оформляем заказ")
    def create_order():
        return order.order_create(213, 'shop', 'Ивано Ива ИВ', '19999999999', 
                                  'email@gmail.com')

    @allure.step("Проверяем успешное оформление заказа")
    def check_order(order_id):
        res = order.view_order(order_id)
        order.delete_order(order_id)
        assert res == 200

    add_to_cart()
    order_id = create_order()
    check_order(order_id)
