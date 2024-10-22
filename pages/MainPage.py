import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class MainPage:
    def __init__(self, browser, config) -> None:
        self.url = config.get('data', 'ui_url')
        self.token = 'Bearer%20' + config.get('data', 'access_token')
        self.browser = browser

    @allure.step("Перейти на главную страницу и авторизироваться")
    def go_to_page(self) -> None:
        try:
            self.browser.get(self.url)
            current_token = self.browser.get_cookie('access-token').get('value')
            if current_token != str(self.token):
                self.browser.delete_cookie('access-token')
                cookie = {'name': 'access-token', 'value': self.token}
                self.browser.add_cookie(cookie)
                self.browser.refresh()

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Поиск по строке {input}")
    def search(self, input: str) -> None:
        try:
            field = self.browser.find_element(By.CSS_SELECTOR, 
                                              '[class="header-search__input"]')
            field.send_keys(input)
            btn = self.browser.find_element(By.CSS_SELECTOR, 
                                            '[class="header-search__button"]')
            btn.click()

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self) -> None:
        try:
            buy_btn = self.browser.find_element(By.CSS_SELECTOR, 
                                                '[class="button action-button blue"]')
            act = ActionChains(self.browser)
            act.move_to_element(buy_btn).perform()
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 
                                             '[class="button action-button blue"]')))
            buy_btn.click()

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Получить текущее URL")
    def get_current_url(self) -> str:
        try:
            WebDriverWait(self.browser, 5).until(
                EC.any_of(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '[class="catalog-empty-result__icon"]')),
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, '[class="search-page__found-message"]'))
                ))
            return self.browser.current_url

        except Exception as e:
            print("An error occurred:", str(e))

    @allure.step("Отменить все заказы")
    def cancel_orders(self) -> None:
        self.browser.get(self.url + '/profile/orders')
        try:
            while True:
                elements = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, 
                         '[class="button order-card__cancel light-blue"]')))

                if not elements:
                    print('No more orders to cancel.')
                    break

                for element in elements:
                    act = ActionChains(self.browser)
                    act.move_to_element(element).perform()

                    WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable(element)).click()
                    WebDriverWait(self.browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, 
                             '[class="dialog__button chg-app-button '
                             'chg-app-button--primary chg-app-button--extra-large '
                             'chg-app-button--brand-blue"]'))).click()
                    WebDriverWait(self.browser, 10).until(EC.staleness_of(element))
                    break

        except Exception as e:
            print('All orders are cancelled:', e)