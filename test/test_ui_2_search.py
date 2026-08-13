import pytest
import allure
from pages.main_page import MainPage


@pytest.mark.ui
@allure.feature("UI Поиск")
@allure.story("Поиск товара")
@allure.title("Проверка успешного поиска товара 'Шаверма'")
def test_search_product_ui(driver) -> None:
    main_page = MainPage(driver)
    main_page.search_product("Шаверма")
    assert main_page.is_product_visible_in_results() is True
