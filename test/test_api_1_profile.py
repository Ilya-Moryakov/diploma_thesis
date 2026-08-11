import pytest
import requests
import allure
from config import BASE_URL, AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE


@pytest.mark.api
@allure.feature("API Профиль")
class TestProfileApi:

    @pytest.fixture(autouse=True)
    def setup_session(self) -> None:
        self.session = requests.Session()
        self.session.cookies.set(AUTH_COOKIE_NAME, AUTH_COOKIE_VALUE,
                                 domain=".yandex.ru")
        self.session.headers.update({"Content-Type": "application/json"})

    @allure.story("Просмотр профиля")
    @allure.title("Проверка успешного статус-кода 200 при запросе профиля")
    @allure.step("Отправка GET запроса на эндпоинт профиля")
    def test_get_profile_status_code(self) -> None:
        url = f"{BASE_URL}/web-api/passport/profile"
        response = self.session.get(url)
        assert response.status_code == 200
