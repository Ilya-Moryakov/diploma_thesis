import pytest
import allure
from pages.main_page import MainPage


@pytest.mark.ui
@allure.feature("UI Корзина")
@allure.story("Изменение количества")
@allure.title("Проверка изменения счетчика корзины при увеличении количества")
def test_update_cart_quantity_ui(driver) -> None:
    main_page = MainPage(driver)

    main_page.search_product("Шаверма")
    main_page.add_product_to_cart()

    main_page.change_cart_item_quantity(2)

    assert main_page.get_cart_counter_text("2") == "2"
