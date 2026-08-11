import pytest
import requests
import allure
from config import BASE_URL, CART_PARAMS, AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE


@pytest.mark.api
@allure.feature("API Корзина")
class TestCartUpdateApi:

    @pytest.fixture(autouse=True)
    def setup_session(self) -> None:
        self.session = requests.Session()
        self.session.cookies.set(AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE,
                                 domain=".yandex.ru")
        self.session.headers.update({"Content-Type": "application/json"})

    @allure.story("Изменение количества")
    @allure.title("Проверка изменения количества товара в корзине на 50 штук")
    @allure.step("Отправка PUT запроса на изменение количества товара")
    def test_update_item_quantity_status(self) -> None:
        id_cart = "3006511283"
        url = f"{BASE_URL}/api/v1/cart/{id_cart}"

        params = CART_PARAMS.copy()
        params["placeSlug"] = "vlavashe_rmnxc"

        payload = {
            "quantity": 50,
            "item_options": []
        }

        response = self.session.put(url, params=params, json=payload)

        assert response.status_code < 500, \
            (f"Сервер Яндекса упал с критической ошибкой: "
             f"{response.status_code}")
