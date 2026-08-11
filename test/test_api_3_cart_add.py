import pytest
import requests
import allure
from config import BASE_URL, CART_PARAMS, AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE


@pytest.mark.api
@allure.feature("API Корзина")
class TestCartAddApi:

    @pytest.fixture(autouse=True)
    def setup_session(self) -> None:
        self.session = requests.Session()
        self.session.cookies.set(AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE,
                                 domain=".yandex.ru")
        self.session.headers.update({"Content-Type": "application/json"})

    @allure.story("Добавление товара")
    @allure.title("Проверка успешного добавления товара в корзину "
                  "(Status 200/201)")
    @allure.step("Отправка POST запроса на добавление товара 'Шаверма'")
    def test_add_item_to_cart_status(self) -> None:
        url = f"{BASE_URL}/api/v1/cart"
        payload = {
            "quantity": 1,
            "place_slug": "vlavashe_rmnxc",
            "place_business": "restaurant",
            "item_options": [],
            "item_id": 3006511283
        }
        response = self.session.post(url, params=CART_PARAMS, json=payload)
        assert response.status_code in [200, 201]
