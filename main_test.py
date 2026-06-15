# test_regtorg.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from conftest import generate_a_email


# ====================== Успешная регистрация ======================
@pytest.mark.registration
@pytest.mark.smoke
def test_successful_registration(browser, go_to_registration):
    wait = WebDriverWait(browser, 10)

    ActionChains(browser).move_to_element(
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[src="/imgs/but_reg.gif"]')))
    ).perform()

    browser.find_element(By.NAME, "_name").send_keys('asdsadsadsadsad')
    browser.find_element(By.NAME, "_fio").send_keys('sadfsadsadsad')
    browser.find_element(By.NAME, "_login").send_keys(generate_a_email())
    browser.find_element(By.NAME, "_password").send_keys('123123')
    browser.find_element(By.NAME, "_password2").send_keys('123123')

    browser.find_element(By.NAME, "form_reg").submit()

    # Проверка успешной регистрации
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Выход")))
    assert "Выход" in browser.page_source


# ====================== Успешная авторизация ======================
@pytest.mark.authorization
@pytest.mark.smoke
def test_successful_authorization(browser):
    wait = WebDriverWait(browser, 12)
    email = generate_a_email()

    # --- Регистрация ---
    browser.find_element(By.LINK_TEXT, "Регистрация").click()

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[src="/imgs/but_reg.gif"]')))

    browser.find_element(By.NAME, "_name").send_keys('Test User')
    browser.find_element(By.NAME, "_fio").send_keys('Test Full Name')
    browser.find_element(By.NAME, "_login").send_keys(email)
    browser.find_element(By.NAME, "_password").send_keys('123123')
    browser.find_element(By.NAME, "_password2").send_keys('123123')

    browser.find_element(By.NAME, "form_reg").submit()

    # Ожидаем выход после регистрации
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Выход"))).click()

    # --- Авторизация ---
    wait.until(EC.presence_of_element_located((By.NAME, "login"))).send_keys(email)
    browser.find_element(By.NAME, "passwd").send_keys('123123')
    
    browser.find_element(By.CSS_SELECTOR, 'input[src="/imgs/but_in.gif"]').click()

    # Проверка успешного входа
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Выход")))
    assert "Выход" in browser.page_source


# ====================== Неуспешная регистрация ======================
@pytest.mark.registration
@pytest.mark.negative
def test_failed_registration(browser, go_to_registration):
    wait = WebDriverWait(browser, 10)

    ActionChains(browser).move_to_element(
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[src="/imgs/but_reg.gif"]')))
    ).perform()

    browser.find_element(By.NAME, "_name").send_keys('aaaa11111')
    browser.find_element(By.NAME, "_fio").send_keys('aaaaaa111111')
    browser.find_element(By.NAME, "_login").send_keys('invalid_email.com')
    browser.find_element(By.NAME, "_password").send_keys('12345')
    browser.find_element(By.NAME, "_password2").send_keys('12345')

    browser.find_element(By.NAME, "form_reg").submit()

    try:
        error = wait.until(
            EC.presence_of_element_located((By.XPATH, "//font[@color='red' and contains(text(), 'Ошибка') or contains(text(), 'E-mail')]"))
        )
        assert error.is_displayed()
    except TimeoutException:
        pytest.fail("Не отобразилось сообщение об ошибке при некорректной регистрации")


# ====================== Неуспешная авторизация ======================
@pytest.mark.authorization
@pytest.mark.negative
def test_failed_authorization(browser):
    wait = WebDriverWait(browser, 10)

    # Убеждаемся, что мы на главной странице / странице входа
    if "login" not in browser.current_url:
        browser.find_element(By.LINK_TEXT, "Вход").click()   # или как у вас называется ссылка на вход

    wait.until(EC.presence_of_element_located((By.NAME, "login"))).send_keys('invalid@email.com')
    browser.find_element(By.NAME, "passwd").send_keys('wrongpassword')
    
    browser.find_element(By.CSS_SELECTOR, 'input[src="/imgs/but_in.gif"]').click()

    try:
        error = wait.until(
            EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Неверный') or contains(text(), 'ошибка') or contains(text(), 'Ошибка')]")),
                EC.presence_of_element_located((By.XPATH, "//font[@color='red']"))
            )
        )
        assert error.is_displayed()
    except TimeoutException:
        pytest.fail("Не отобразилось сообщение об ошибке при неудачной авторизации")


# ====================== E2E: Регистрация + Покупка ======================
@pytest.mark.e2e
@pytest.mark.smoke
def test_successful_registration_and_purchase(browser):
    wait = WebDriverWait(browser, 15)
    email = generate_a_email()

    # Регистрация
    browser.find_element(By.LINK_TEXT, "Регистрация").click()
    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[src="/imgs/but_reg.gif"]')))

    browser.find_element(By.NAME, "_name").send_keys('Buyer Test')
    browser.find_element(By.NAME, "_fio").send_keys('Buyer Test Full')
    browser.find_element(By.NAME, "_login").send_keys(email)
    browser.find_element(By.NAME, "_password").send_keys('Ww161719')
    browser.find_element(By.NAME, "_password2").send_keys('Ww161719')
    browser.find_element(By.NAME, "form_reg").submit()

    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Выход")))

    # Переход в каталог
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(), 'Товары и услуги')]")
    )).click()

    # Бытовая техника
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Бытовая техника"))).click()
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Аудиотехника"))).click()

        # === УПРОЩЁННЫЙ ПОИСК ТОВАРА ===
    wait = WebDriverWait(browser, 12)

    # Переход в каталог
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(), 'Товары и услуги')]")
    )).click()

    # Бытовая техника → Аудиотехника
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Бытовая техника"))).click()
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Аудиотехника"))).click()

    # Покупка товара
    try:
        # Кнопка "Купить" по onclick (самый стабильный сейчас)
        buy_button = wait.until(
            EC.element_to_be_clickable((
                By.XPATH, '//a[contains(@onclick, "ChangeBasket(553196")]'
            ))
        )
        buy_button.click()
        print("✅ Купить нажато")
        
    except TimeoutException:
        browser.save_screenshot("buy_error.png")
        pytest.fail("Не найдена кнопка Купить у Микрофон MB-7K")

    except TimeoutException:
        print("❌ Всё равно не найдено. Делаем отладку...")

        # === ОТЛАДКА ===
        browser.save_screenshot("buy_timeout.png")
        
        print("Текущий URL:", browser.current_url)
        
        # Сколько вообще кнопок "Купить" на странице
        all_buy = browser.find_elements(By.XPATH, '//a[@class="nbut" or contains(text(),"Купить")]')
        print(f"Найдено кнопок Купить: {len(all_buy)}")

        # Ищем конкретно около микрофона
        near = browser.find_elements(By.XPATH, 
            '//a[contains(text(),"Микрофон MB-7K")]/following::a[contains(@class,"nbut") or contains(text(),"Купить")]')
        print(f"Кнопок Купить рядом с товаром: {len(near)}")
        
        pytest.fail("Не удалось нажать Купить у Микрофон MB-7K")
    
    # Оформить заказ
    wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Оформить заказ"))).click()

    assert any(word in browser.page_source.lower() for word in ["заказ", "оформлен", "корзина"])