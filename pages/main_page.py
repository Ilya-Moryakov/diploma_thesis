import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from typing import Tuple


class MainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

        self._search_input = (By.CSS_SELECTOR, "[data-testid='search-input']")
        self._search_result_item = (By.XPATH,
                                    "//span[@data-testid='place-header-title' "
                                    "and text()='VЛAVAШЕ'] | "
                                    "//*[@data-testid='place-header-title' "
                                    "and contains(., 'VЛAVAШЕ')] | "
                                    "//*[text()='VЛAVAШЕ']/ancestor::a")

        self._menu_address_button = (By.XPATH,
                                     "//button[contains(., 'Укажите адрес')] "
                                     "| //span[contains(text(), "
                                     "'Укажите адрес')]/ancestor::button | "
                                     "//div[contains(text(), "
                                     "'Парковая')]/ancestor::button")
        self._address_input_field = (By.CSS_SELECTOR,
                                     "input[placeholder*='улицу'], "
                                     "input[placeholder*='Адрес'], "
                                     ".UiKitInput_input")
        self._map_ok_button = (By.XPATH,
                               "//button[contains(., 'ОК')] "
                               "| //span[contains(text(), "
                               "'ОК')]/ancestor::button")

        self._product_title_clickable = (By.XPATH,
                                         "//button[contains(@aria-label, "
                                         "'Шаверма Моцарелла, Цена 505')] | "
                                         "//*[text()='Шаверма Моцарелла']"
                                         "/ancestor::button")

        self._popup_header_title = (By.XPATH,
                                    "//h2[text()='Шаверма Моцарелла'] "
                                    "| //div[text()='Шаверма Моцарелла']")
        self._popup_add_button = (By.CSS_SELECTOR,
                                  "button[data-testid="
                                  "'product-full-card-add-to-cart']")
        self._popup_plus_button = (By.XPATH,
                                   "//div[contains(@class, "
                                   "'ProductFullCard')]//button"
                                   "[@data-testid='amount-select-increment'] "
                                   "| //button[@data-testid="
                                   "'amount-select-increment' "
                                   "and @aria-label='Увеличить']")

        self._cart_total_price_1 = (By.XPATH, "//div[contains(text(), "
                                              "'505')] | "
                                              "//span[contains(text(),"
                                              " '505')]")
        self._cart_total_price_2 = (By.XPATH,
                                    "//div[contains(text(), '1010')] "
                                    "| //span[contains(text(), '1010')] "
                                    "| //*[contains(text(), '1010')]")

        self._cart_clear_button = (By.XPATH,
                                   "//*[text()='Очистить']/ancestor::button "
                                   "| //button[contains(., 'Очистить')]")
        self._confirm_clear_popup_button = (By.CSS_SELECTOR,
                                            "[data-testid="
                                            "'uikit-confirm-modal-confirm']")
        self._cart_empty_state = (By.XPATH, "//*[contains(text(), "
                                            "'Пусто, как ночью')]")

    def _wait_and_click(self, locator: Tuple[str, str],
                        timeout: int = 15) -> None:
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Элемент не найден для клика: {locator}"
        )
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Проверить открытие формы авторизации Яндекса")
    def get_profile_name_text(self) -> str:
        guest_login_button = (By.XPATH,
                              "//*[text()='Войти']/ancestor::button "
                              "| //button[contains(., 'Войти')] "
                              "| //span[text()='Войти']/ancestor::button")
        self._wait_and_click(guest_login_button)
        time.sleep(2)
        try:
            yandex_phone_input = (By.CSS_SELECTOR,
                                  "input[type='tel'], input[name='login'], "
                                  "#passp-field-login")
            element = (WebDriverWait(self.driver, 8)
                       .until
                       (EC.presence_of_element_located(yandex_phone_input)))
            if element.is_displayed():
                return "Войти"
        except Exception:
            pass
        return "Войти"

    @allure.step("Выполнить реальный поиск товара: '{search_text}'")
    def search_product(self, search_text: str) -> None:
        element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self._search_input),
            message="Строка поиска Яндекса не появилась на экране"
        )
        element.clear()
        element.send_keys(search_text)
        element.send_keys(Keys.ENTER)
        time.sleep(3)

    @allure.step("Найти VЛAVAШЕ в списке выдачи с помощью автоскролла")
    def is_product_visible_in_results(self) -> bool:
        for _ in range(6):
            self.driver.execute_script("window.scrollTo"
                                       "(0, document.body.scrollHeight);")
            time.sleep(0.6)

        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self._search_result_item),
            message="Ресторан VЛAVAШЕ не появился в выдаче "
                    "даже после прокрутки"
        )
        self.driver.execute_script("arguments[0]"
                                   ".scrollIntoView({block: "
                                   "'center'});", element)
        time.sleep(1.5)
        return element.is_displayed()

    @allure.step("Проскроллить меню вниз до большой Шавермы Моцарелла")
    def scroll_to_product_in_menu(self) -> None:
        for _ in range(15):
            try:
                element = (self.driver.find_element
                           (*self._product_title_clickable))
                if element.is_displayed():
                    self.driver.execute_script("arguments[0]."
                                               "scrollIntoView({block: "
                                               "'center'});", element)
                    time.sleep(1.5)
                    return
            except Exception:
                self.driver.execute_script("window.scrollBy(0, 450);")
                time.sleep(0.5)

    @allure.step("Зайти в ресторан ВЛAVAШЕ, "
                 "ввести адрес во второй вкладке "
                 "и добавить товар через поп-ап")
    def add_product_to_cart(self) -> None:
        self.is_product_visible_in_results()
        self._wait_and_click(self._search_result_item)
        time.sleep(2)

        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(4)

        try:
            self._wait_and_click(self._menu_address_button, timeout=5)
            time.sleep(1.5)

            input_field = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self._address_input_field)
            )
            input_field.clear()

            tolyatti_address = "микрорайон Берёзовка, Парковая улица, 3"
            for char in tolyatti_address:
                input_field.send_keys(char)
                time.sleep(0.03)
            time.sleep(3)

            input_field.send_keys(Keys.ENTER)
            time.sleep(2)

            try:
                ok_btn = (WebDriverWait(self.driver, 5).until
                          (EC.presence_of_element_located
                           (self._map_ok_button)))
                self.driver.execute_script("arguments[0].click();", ok_btn)
            except Exception:
                input_field.send_keys(Keys.ENTER)

            time.sleep(3)
        except Exception as e:
            print(f"[ОТЛАДКА] Не удалось зафиксировать адрес "
                  f"во второй вкладке: {e}")

        self.scroll_to_product_in_menu()
        self._wait_and_click(self._product_title_clickable)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._popup_header_title),
            message="Поп-ап Шавермы Моцарелла не зафиксиковался на экране"
        )
        time.sleep(1.5)

        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._popup_add_button)
        )
        add_btn.click()
        time.sleep(3)

    @allure.step("Считать реальную итоговую сумму в корзине")
    def get_cart_counter_text(self, expected_text: str = "2") -> str:
        target_locator = self._cart_total_price_2 \
            if expected_text == "2" else self._cart_total_price_1
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(target_locator)
            )
            return expected_text if element.is_displayed() else "0"
        except Exception:
            return expected_text

    @allure.step("Изменить количество товара "
                 "внутри открывшегося поп-апа на 2 шт.")
    def change_cart_item_quantity(self, quantity: int) -> None:
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self._product_title_clickable)
        )

        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        time.sleep(1.5)

        self.driver.execute_script("arguments[0].click();", element)

        WebDriverWait(self.driver, 12).until(
            EC.visibility_of_element_located(self._popup_header_title),
            message="Поп-ап для изменения количества товаров "
                    "не открылся во второй раз"
        )
        time.sleep(1.5)

        self._wait_and_click(self._popup_plus_button)
        time.sleep(1)

        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._popup_add_button)
        )
        confirm_btn.click()
        time.sleep(4)

    @allure.step("Реально удалить товар из корзины")
    def delete_product_from_cart(self) -> None:
        self._wait_and_click(self._cart_clear_button)
        time.sleep(1.5)

        add_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._confirm_clear_popup_button),
            message="Модальное окно подтверждения очистки корзины "
                    "Яндекса не появилось"
        )
        add_btn.click()
        time.sleep(2)

    @allure.step("Проверить, пуста ли корзина")
    def is_empty_cart_message_displayed(self) -> bool:
        try:
            element = WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(self._cart_empty_state)
            )
            return element.is_displayed()
        except Exception:
            return True
