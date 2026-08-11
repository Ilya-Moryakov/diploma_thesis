import pytest
import allure
from pages.main_page import MainPage


@pytest.mark.ui
@allure.feature("UI Корзина")
@allure.story("Удаление товара")
@allure.title("Проверка удаления товара и очистки корзины")
def test_delete_from_cart_ui(driver) -> None:
    main_page = MainPage(driver)
    main_page.search_product("Шаверма")
    main_page.add_product_to_cart()
    main_page.delete_product_from_cart()
    assert main_page.is_empty_cart_message_displayed() is True
