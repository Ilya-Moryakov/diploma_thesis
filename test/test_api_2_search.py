import pytest
import requests
import allure
from config import BASE_URL, CART_PARAMS


@pytest.mark.api
@allure.feature("API Поиск")
class TestSearchApi:

    @pytest.fixture(autouse=True)
    def setup_session(self) -> None:
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    @allure.story("Поиск товара")
    @allure.title("Проверка статус-кода 200 при поиске Шавермы")
    @allure.step("Отправка POST запроса на поиск 'Шаверма' "
                 "с передачей геолокации")
    def test_search_product_status_code(self) -> None:
        url = f"{BASE_URL}/eats/v1/full-text-search/v1/search"

        payload = {
            "text": "Шаверма",
            "location": {
                "latitude": float(CART_PARAMS["latitude"]),
                "longitude": float(CART_PARAMS["longitude"])
            }
        }

        response = self.session.post(url, json=payload)
        assert response.status_code == 200
