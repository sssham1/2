# conftest.py
import pytest
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- Pytest command-line options ----------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")
    parser.addoption("--language", action="store", default="en", help="User language")

# ---------- Helper functions ----------
def generate_a_email(min_a=1, max_a=30, domain="gmail.com"):
    name = 'g' * random.randint(min_a, max_a)
    return f"{name}@{domain}"

# ---------- Fixtures ----------
@pytest.fixture(scope="function")
def browser(request):
    """Fixture to initialize and quit the browser."""
    browser_name = request.config.getoption("--browser")
    language = request.config.getoption("--language")

    # Optional: add language preference if needed (e.g., for Chrome)
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if language:
            options.add_experimental_option('prefs', {'intl.accept_languages': language})
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if language:
            options.set_preference("intl.accept_languages", language)
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.get("https://www.regtorg.ru/")
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def go_to_registration(browser):
    """Navigate to registration page."""
    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Регистрация"))
    ).click()
    return browser