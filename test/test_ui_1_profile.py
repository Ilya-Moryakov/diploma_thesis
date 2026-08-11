import pytest
import allure
from pages.main_page import MainPage


@pytest.mark.ui
@allure.feature("UI Профиль")
@allure.story("Отображение имени")
@allure.title("Проверка открытия формы профиля в гостевом режиме")
def test_view_profile_ui(driver) -> None:
    main_page = MainPage(driver)

    assert main_page.get_profile_name_text() == "Войти"
