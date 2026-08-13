import pytest
import allure
from pages.main_page import MainPage


@pytest.mark.ui
@allure.feature("UI Корзина")
@allure.story("Добавление товара")
@allure.title("Проверка появления товара в корзине после добавления")
def test_add_to_cart_ui(driver) -> None:
    main_page = MainPage(driver)

    main_page.search_product("Шаверма")

    main_page.add_product_to_cart()

    assert main_page.get_cart_counter_text("1") == "1"
