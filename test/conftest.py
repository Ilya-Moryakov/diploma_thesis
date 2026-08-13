import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import BASE_URL


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")

    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2
    })

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    driver.get(BASE_URL)
    time.sleep(2)

    yield driver
    driver.quit()
