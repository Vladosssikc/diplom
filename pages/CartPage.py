import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class CartPage:
    def __init__(self, browser, config) -> None:
        self.url = config.get('data', 'ui_url') + '/cart'
        self.token = 'Bearer%20' + config.get('data', 'access_token')
        self.browser = browser

    @allure.step("Перейти в корзину и авторизироваться")
    def go_to_cart(self) -> int:
        try:
            self.browser.get(self.url)
            current_token = self.browser.get_cookie('access-token').get('value')
            if current_token != str(self.token):
                self.browser.delete_cookie('access-token')
                cookie = {'name': 'access-token', 'value': self.token}
                self.browser.add_cookie(cookie)
                self.browser.refresh()

            WebDriverWait(self.browser, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'cart-content')))
            count = 0
            try:
                elements = self.browser.find_elements(By.CLASS_NAME, 'cart-item')
                for element in elements:
                    count += 1
            except Exception as e:
                print("No elements of such class found:", e)

            return count

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Перейти на страницу оформления заказа")
    def go_to_order_page(self) -> None:
        try:
            order_btn = self.browser.find_element(By.CSS_SELECTOR, 
                                                  '[class="button cart-sidebar__order-button blue"]')
            act = ActionChains(self.browser)
            act.move_to_element(order_btn).perform()
            WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable(order_btn))
            order_btn.click()

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Выбрать город в России")
    def choose_city_in_rus(self) -> None:
        try:
            self.browser.find_element(By.CLASS_NAME, 'order-page__city').click()
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'app-select__icon'))).click()
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="__layout"]/div/div[2]/div/div[2]/div/div[2]/div/div[2]/ul/li[3]'))
            ).click()
            self.browser.find_element(By.CLASS_NAME, 'city-modal__popular-item').click()

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Выбрать пункт выдачи")
    def choose_pickup_point(self) -> None:
        WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="step1"]/div[2]/div/section[2]/div[2]'))).click()
        try:
            btn = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="step1"]/div[2]/section/div/div')))
            if btn:
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(btn)).click()
                select = WebDriverWait(self.browser, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__layout"]/div/div[5]/div/div[2]/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/button[1]')))
                WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(select)).click()

        except TimeoutException:
            print("Map not found, proceeding to check for selected map layout.")

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pvz-selected__map-layout")))

    @allure.step("Выбрать {option} как способ оплаты")
    def choose_payment_method(self, option: str) -> None:
        """
        Выбрать способ оплаты для заказа.

        Args:
            option (str): Способ оплаты ('sbp', 'webcard', 'face-to-face').
        """
        try:
            pay = self.browser.find_element(By.CLASS_NAME, 'payments__list')
            act = ActionChains(self.browser)
            act.move_to_element(pay).perform()

            if option == 'sbp':
                sbp = WebDriverWait(self.browser, 15).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="step2"]/div[2]/div/div[2]/button[2]')))
                if "payments-item payments__item payments-item--active" not in sbp.get_attribute("class").split():
                    sbp.click()

            elif option == 'webcard':
                card = WebDriverWait(self.browser, 15).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="step2"]/div[2]/div/div[2]/button[1]')))
                if "payments-item payments__item payments-item--active" not in card.get_attribute("class").split():
                    card.click()

            elif option == 'face-to-face':
                face = WebDriverWait(self.browser, 15).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="step2"]/div[2]/div/div[2]/button[3]')))
                if "payments-item payments__item payments-item--active" not in face.get_attribute("class").split():
                    face.click()

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Оформить заказ")
    def checkout_order(self) -> bool:
        try:
            self.browser.implicitly_wait(3)
            WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="__layout"]/div/div[3]/div[1]/div[2]/div/div/div[2]/div/div[3]/button'))).click()

            if WebDriverWait(self.browser, 10).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[class="pay-by-card"]')),
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[class="thank-you-page"]'))
                )):
                return True
            else:
                return False

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Очистить корзину")
    def clear_cart(self) -> None:
        if self.browser.current_url != self.url:
            self.go_to_cart()
        try:
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'delete-many'))).click()
        except Exception as e:
            print(e, 'No cart items found')