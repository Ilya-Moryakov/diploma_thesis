import pytest
import requests
import allure
from config import BASE_URL, CART_PARAMS, AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE


@pytest.mark.api
@allure.feature("API Корзина")
class TestCartDeleteApi:

    @pytest.fixture(autouse=True)
    def setup_session(self) -> None:
        self.session = requests.Session()
        self.session.cookies.set(AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE,
                                 domain=".yandex.ru")
        self.session.headers.update({"Content-Type": "application/json"})

    @allure.story("Удаление товара")
    @allure.title("Проверка успешного удаления товара и очистки корзины")
    @allure.step("Отправка DELETE запроса для удаления товара")
    def test_delete_item_from_cart_status(self) -> None:
        url = f"{BASE_URL}/api/v2/cart"

        params = CART_PARAMS.copy()
        params["placeSlug"] = "vlavashe_rmnxc"

        response = self.session.delete(url, params=params)
        assert response.status_code in [200, 204]
