import allure
from API.api_client import ApiClient   

class Cart(ApiClient):
    def __init__(self, config):
        super().__init__(config)
        self.productID = int(config.get('data', 'productID'))

    @allure.step("API - Добавить товар в корзину")
    def add_to_cart(self) -> int:
        _body = {
            "id": self.productID,
            "adData": {
                "item_list_name": "articles-slug",
                "product_shelf": "Блок товара в статьях"
            }
        }
        response = self.post_request(self.url + '/cart/product', body=_body)
        return response.status_code

    @allure.step("API - Просмотреть корзину")
    def view_cart(self) -> int:
        response = self.get_request(self.url + '/cart')
        return response.json()['products'][0]['goodsId']
