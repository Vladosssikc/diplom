import requests
import allure


class ApiClient:
    def __init__(self, config):
        self.url = config.get('data', 'api_url')
        self.url2 = config.get('data', 'api_url2')
        self.access_token = config.get('data', 'access_token')
        self.headers = {'Authorization': 'Bearer ' + self.access_token}
        self.session = requests.Session()

    @allure.step("API - Отправить GET запрос")
    def get_request(self, url: str, params: dict = None) -> requests.Response:
        if params is None:
            params = {}
        try:
            response = self.session.get(
                url, headers=self.headers, params=params
            )
            return response
        except requests.RequestException as e:
            print("An error occurred:", e.response)
            return None

    @allure.step("API - Отправить POST запрос")
    def post_request(
        self, url: str, params: dict = None, body: dict = None
    ) -> requests.Response:
        if params is None:
            params = {}
        if body is None:
            body = {}
        try:
            response = self.session.post(
                url, headers=self.headers, params=params, json=body
            )
            return response
        except requests.RequestException as e:
            print("An error occurred:", e.response)
            return None

    @allure.step("API - Отправить DELETE запрос")
    def delete_request(self, url: str) -> requests.Response:
        try:
            response = self.session.delete(url, headers=self.headers)
            return response
        except requests.RequestException as e:
            print("An error occurred:", e.response)
            return None
