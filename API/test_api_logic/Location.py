import allure
from API.api_client import ApiClient 

class Location(ApiClient):
    @allure.step("API - Отправить запрос на поиск адреса по ключевому слову")
    def suggest_address_street(self, country_code: str = 'RU') -> str:
        my_params = {
            'countryCode': country_code,
            'count': 1,
            'query': 'ленин'
        }
        response = self.get_request(
            self.url + '/location/suggest/address', params=my_params
        )
        return response.json()[0]['address']

    @allure.step("API - Получить информацию об адресе получения")
    def suggest_address_house(self, country_code: str = 'RU') -> dict:
        my_params = {
            'countryCode': country_code,
            'count': 2,
            'query': self.suggest_address_street()
        }
        response = self.get_request(
            self.url + '/location/suggest/address', params=my_params
        )
        return response.json()

    @allure.step("API - Получить информацию о магазине")
    def shops_info(self, city_id: int) -> dict:
        my_params = {
            'isCheckout': True,
            'userType': 'individual',
            'cityId': city_id
        }
        response = self.get_request(
            self.url + '/order-info/shop', params=my_params
        )
        return response.json()
