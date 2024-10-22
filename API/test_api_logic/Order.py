import allure
from API.api_client import ApiClient 
from API.test_api_logic.Location import Location


class Order(ApiClient):
    def __init__(self, config):
        super().__init__(config)
        self.location = Location(config)

    @allure.step("API - Получить тело запроса")
    def order_body(
        self, city_id: int, shipment_type: str, username: str,
        userphone: str, useremail: str
    ) -> dict:
        shops_data = self.location.shops_info(city_id)['data']['items'][0]
        address_data = self.location.suggest_address_house()
        _body = {
            "cityId": city_id,
            "paymentType": 'sbp',
            "useAmountBonusPay": 0,
            "user": {
                "type": "individual",
                "name": username,
                "phone": userphone,
                "email": useremail,
                "emailNotifications": True,
                "smsNotifications": True
            },
            "legalEntity": None,
            "shelf": "",
            "listName": "",
            "deliveryDate": shops_data['deliveryDate'],
            "orderType": "order",
            "bonusPayment": 0
        }

        if shipment_type == 'shop':
            _body["shipment"] = {
                "type": 'shop',
                "id": 19,
                "pointId": shops_data['id']
            }
            _body["address"] = {
                "index": None,
                "street": None,
                "house": None,
                "building": None,
                "block": None,
                "apartment": None,
                "fullAddress": None,
                "comment": None
            }
        elif shipment_type == 'courier':
            _body["shipment"] = {
                "type": 'courier',
                "id": 53,
                "address": {
                    "address": shops_data['address'],
                    "apartment": None,
                    "building": None,
                    "cityId": city_id,
                    "house": None,
                    "housing": None,
                    "street": None,
                    "zip": '123060',
                    "fullAddress": shops_data['address'],
                    "index": None,
                    "block": None,
                    "comment": None
                },
                "isLoadedData": False,
                "deliveryId": 19,
                "providerPickpointId": shops_data['providerPickpointId'],
            }
            _body["address"] = {
                "index": address_data[0]['postcode'],
                "street": address_data[1]['street']['fullName'],
                "house": address_data[1]['houseDetails']['house'],
                "building": None,
                "block": None,
                "apartment": None,
                "fullAddress": address_data[1]['addressFull'],
                "comment": None,
                "coordinates": {
                    "latitude": address_data[1]['coordinates']['latitude'],
                    "longitude": address_data[1]['coordinates']['longitude']
                }
            }
        elif shipment_type == 'post':
            _body["shipment"] = {
                "type": 'post',
                "id": 0
            }
            _body["address"] = {
                "index": address_data[0]['postcode'],
                "street": address_data[1]['street']['fullName'],
                "house": address_data[1]['houseDetails']['house'],
                "building": None,
                "block": None,
                "apartment": None,
                "fullAddress": address_data[1]['addressFull'],
                "comment": None,
                "coordinates": {
                    "latitude": address_data[1]['coordinates']['latitude'],
                    "longitude": address_data[1]['coordinates']['longitude']
                }
            }
        return _body

    @allure.step("API - Создать данные для заказа")
    def orders_calculate(
        self, city_id: int, shipment_type: str, username: str,
        userphone: str, useremail: str
    ) -> int:
        _body = self.order_body(
            city_id, shipment_type, username, userphone, useremail
        )
        response = self.post_request(
            self.url + '/orders-calculate', body=_body
        )
        return response.status_code

    @allure.step("API - Оформить заказ")
    def order_create(
        self, city_id: int, shipment_type: str, username: str,
        userphone: str, useremail: str
    ) -> str:
        _body = self.order_body(
            city_id, shipment_type, username, userphone, useremail
        )
        calculation_status = self.orders_calculate(
            city_id, shipment_type, username, userphone, useremail
        )
        if calculation_status != 200:
            raise Exception(
                f"Order calculation failed with status code: {calculation_status}"
            )

        response = self.post_request(self.url + '/orders', body=_body)

        if 'id' in response.json():
            return response.json()['id']
        else:
            print(
                "Warning: 'id' not found in response. Response content:",
                response.json()
            )
            return ''

    @allure.step("API - Просмотреть заказ")
    def view_order(self, order_id: int) -> int:
        response = self.get_request(self.url2 + '/orders/' + str(order_id))
        return response.status_code

    @allure.step("API - Удалить заказ")
    def delete_order(self, order_id: int) -> int:
        response = self.delete_request(self.url + '/orders/' + str(order_id))
        return response.status_code if response else None
