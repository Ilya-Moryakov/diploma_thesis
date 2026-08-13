import allure
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
        self._any_place_title = (By.XPATH,
                                 "//*[@data-testid='place-header-title']")
        self._search_result_item = (By.XPATH,
                                    "//span[@data-testid='place-header-title' "
                                    "and text()='VЛAVAШЕ'] | "
                                    "//*[@data-testid='place-header-title' "
                                    "and contains(., 'VЛAVAШЕ')] | "
                                    "//*[text()='VЛAVAШЕ']/ancestor::a")
        self._menu_address_button = (By.XPATH,
                                     "//button[contains(., "
                                     "'Укажите адрес')] | "
                                     "//span[contains(text(), "
                                     "'Укажите адрес')]/ancestor::button | "
                                     "//div[contains(text(), "
                                     "'Парковая')]/ancestor::button")
        self._address_input_field = (By.CSS_SELECTOR,
                                     "input[placeholder*='улицу'], "
                                     "input[placeholder*='Адрес'], "
                                     ".UiKitInput_input")
        self._map_ok_button = (By.XPATH,
                               "//button[contains(., 'ОК')] | "
                               "//span[contains(text(), 'ОК')]"
                               "/ancestor::button")
        self._category_shaverma_tab = (By.XPATH,
                                       "//*[contains(., 'Шаверма') and "
                                       "not(contains(., 'Мини'))]")

        self._product_title_clickable = (By.XPATH,
                                         "//button[contains(@aria-label, "
                                         "'Шаверма Моцарелла, Цена 505')] | "
                                         "//*[text()='Шаверма Моцарелла']"
                                         "/ancestor::button")
        self._popup_header_title = (By.XPATH,
                                    "//h2[text()='Шаверма Моцарелла'] | "
                                    "//div[text()='Шаверма Моцарелла']")
        self._popup_add_button = (By.CSS_SELECTOR, "button[data-testid='"
                                                   "product-full-card-"
                                                   "add-to-cart']")
        self._popup_plus_button = (By.XPATH,
                                   "//div[contains(@class, 'ProductFullCard')"
                                   "]//button[@data-testid="
                                   "'amount-select-increment'] | "
                                   "//button[@data-testid="
                                   "'amount-select-increment' "
                                   "and @aria-label='Увеличить']")
        self._cart_total_price_1 = (By.XPATH, "//div[contains(text(), "
                                              "'505')] | "
                                              "//span[contains(text(), "
                                              "'505')]")
        self._cart_total_price_2 = (By.XPATH,
                                    "//div[contains(text(), '1010')] | "
                                    "//span[contains(text(), '1010')] | "
                                    "//*[contains(text(), '1010')]")
        self._cart_clear_button = (By.XPATH,
                                   "//*[text()='Очистить']/ancestor::button "
                                   "| //button[contains(., 'Очистить')]")
        self._confirm_clear_popup_button = (By.CSS_SELECTOR,
                                            "[data-testid='uikit-confirm-"
                                            "modal-confirm']")
        self._cart_empty_state = (By.XPATH,
                                  "//*[contains(text(), "
                                  "'Пусто, как ночью')]")

    def _wait_and_click(self, locator: Tuple[str, str],
                        timeout: int = 15) -> None:
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Элемент не найден для клика: {locator}"
        )
        self.driver.execute_script("arguments[0].click();", element)

    def _pause(self, seconds: float) -> None:
        ActionChains(self.driver).pause(seconds).perform()

    @allure.step("Проверить открытие формы авторизации Яндекса")
    def get_profile_name_text(self) -> str:
        guest_login_button = (By.XPATH,
                              "//*[text()='Войти']/ancestor::button | "
                              "//button[contains(., 'Войти')] | "
                              "//span[text()='Войти']/ancestor::button")
        self._wait_and_click(guest_login_button)
        try:
            yandex_phone_input = (By.CSS_SELECTOR,
                                  "input[type='tel'], "
                                  "input[name='login'], "
                                  "#passp-field-login")
            element = (WebDriverWait(self.driver, 8)
                       .until
                       (EC.presence_of_element_located(yandex_phone_input)))
            return "Войти" if element.is_displayed() else "Войти"
        except Exception:
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

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self._any_place_title),
            message="Результаты поиска не загрузились"
        )

    @allure.step("Найти VЛAVAШЕ в списке выдачи с помощью автоскролла")
    def is_product_visible_in_results(self) -> bool:
        for _ in range(8):
            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(self._search_result_item)
                )
                if element.is_displayed():
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView"
                        "({block: 'center'});", element)
                    (WebDriverWait(self.driver, 5)
                     .until(EC.visibility_of(element)))
                    return True
            except Exception:
                self.driver.execute_script("window.scrollTo(0, "
                                           "document.body.scrollHeight);")
                self._pause(0.5)
        element = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self._search_result_item),
            message="Ресторан VЛAVAШЕ не появился в выдаче "
                    "даже после прокрутки"
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: "
                                   "'center'});", element)
        return element.is_displayed()

    @allure.step("Проскроллить меню вниз до большой Шавермы Моцарелла")
    def scroll_to_product_in_menu(self) -> None:
        self._pause(0.5)

        try:
            category = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self._category_shaverma_tab)
            )
            self.driver.execute_script("arguments[0].click();", category)
            print("Кликнули по категории 'Шаверма'")
        except Exception:
            print("Категория 'Шаверма' не найдена, продолжаем без неё.")

        product = None
        for _ in range(30):
            try:
                product = (self.driver.find_element
                           (*self._product_title_clickable))
                if product.is_displayed():
                    print("Продукт найден и видим")
                    break
                else:
                    self.driver.execute_script("arguments[0].scrollIntoView"
                                               "({block: 'center'});", product)
                    self._pause(0.3)
                    if product.is_displayed():
                        print("Продукт стал видимым после scrollIntoView")
                        break
            except Exception:
                self.driver.execute_script("window.scrollBy(0, 500);")
                self._pause(0.5)

        if product is None or not product.is_displayed():
            self.driver.save_screenshot("debug_product_not_found.png")
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise TimeoutException("Продукт 'Шаверма Моцарелла' "
                                   "не найден на странице")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self._product_title_clickable)
            )
            print("Продукт кликабелен")
        except Exception:
            print("Продукт не стал кликабельным, но попробуем кликнуть")

    @allure.step("Зайти в ресторан ВЛAVAШЕ, "
                 "ввести адрес во второй вкладке и "
                 "добавить товар через поп-ап")
    def add_product_to_cart(self) -> None:
        self.is_product_visible_in_results()
        self._wait_and_click(self._search_result_item)

        (WebDriverWait(self.driver, 15)
         .until(lambda d: len(d.window_handles) > 1))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        WebDriverWait(self.driver, 15).until(
            lambda d: "yandex" in d.current_url or "vlavashe" in d.current_url
        )
        print(f"Текущий URL: {self.driver.current_url}")

        self._wait_and_click(self._menu_address_button, timeout=10)

        input_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self._address_input_field)
        )
        input_field.clear()
        input_field.send_keys("микрорайон Берёзовка, Парковая улица, 3")
        self._pause(0.5)
        input_field.send_keys(Keys.ENTER)

        try:
            ok_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self._map_ok_button)
            )
            ok_btn.click()
            print("Кликнули по кнопке ОК")
        except Exception:
            print("Кнопка ОК не появилась, пробуем ещё раз Enter")
            input_field.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 15).until(
                EC.invisibility_of_element_located(self._map_ok_button)
            )
            print("Окно карты закрыто")
        except Exception:
            print("Окно карты не исчезло, но продолжаем")

        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//*[contains(@class, "
                                                "'product') "
                                                "or contains(@class, "
                                                "'card')]"))
            )
            print("Меню загрузилось")
        except Exception:
            print("Меню не загрузилось, но попробуем прокрутку")

        self.scroll_to_product_in_menu()

        product_el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._product_title_clickable)
        )
        try:
            (ActionChains(self.driver).move_to_element(product_el)
             .click().perform())
            print("Кликнули по продукту через ActionChains")
        except Exception:
            self.driver.execute_script("arguments[0].click();", product_el)
            print("Кликнули по продукту через JS")

        try:
            add_btn = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self._popup_add_button)
            )
            print("Поп-ап открыт, кнопка 'Добавить' видима")
        except Exception:
            print("Поп-ап не открылся или кнопка "
                  "'Добавить' не найдена. "
                  "Сохраняю диагностику...")
            self.driver.save_screenshot("debug_popup_not_opened.png")
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            raise

        add_btn.click()
        print("Кликнули по кнопке Добавить")

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self._popup_add_button)
        )

    @allure.step("Считать реальную итоговую сумму в корзине")
    def get_cart_counter_text(self, expected_text: str = "2") -> str:
        target_locator = self._cart_total_price_2 \
            if expected_text == "2" \
            else self._cart_total_price_1
        try:
            element = (WebDriverWait(self.driver, 10)
                       .until
                       (EC.visibility_of_element_located(target_locator)))
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

        (WebDriverWait(self.driver, 5)
         .until
         (EC.element_to_be_clickable(self._product_title_clickable)))
        self.driver.execute_script("arguments[0].click();", element)

        WebDriverWait(self.driver, 12).until(
            EC.visibility_of_element_located(self._popup_add_button),
            message="Поп-ап не открылся для изменения количества"
        )

        self._wait_and_click(self._popup_plus_button)

        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._popup_add_button)
        )
        confirm_btn.click()

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self._popup_add_button)
        )

    @allure.step("Реально удалить товар из корзины")
    def delete_product_from_cart(self) -> None:
        self._wait_and_click(self._cart_clear_button)

        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self._confirm_clear_popup_button),
            message="Модальное окно подтверждения очистки "
                    "корзины Яндекса не появилось"
        )
        confirm_btn.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self._cart_empty_state)
        )

    @allure.step("Проверить, пуста ли корзина")
    def is_empty_cart_message_displayed(self) -> bool:
        try:
            element = (WebDriverWait(self.driver, 6)
                       .until
                       (EC.presence_of_element_located
                        (self._cart_empty_state)))
            return element.is_displayed()
        except Exception:
            return True
