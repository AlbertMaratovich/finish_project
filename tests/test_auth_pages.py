from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import config
import time


def test_redirect_to_auth_page(driver):
    """Поверка редиректа на страницу авторизации при переходе по ЕЛК Web URI"""
    driver.get(config.elk_url)
    # Поверяем редирект на страницу авторизации и базовый элемент
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
        in driver.current_url)
    base_element = driver.find_element("id", "card-title")
    assert base_element.is_displayed()


def test_send_code_to_email(driver):
    """Проверяется отправка кода по почте и редиректа на страницу ввода кода со страница авторизации без пароля"""
    # переходим на страницу
    driver.get(config.elk_url)
    # заполняем поле
    auth_field = driver.find_element("id", "address")
    auth_field.clear()
    auth_field.send_keys(config.random_email)
    # нажимаем на кнпоку получить код
    btn_get_code = driver.find_element("id", "otp_get_code")
    btn_get_code.click()
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/authenticate"
                  in driver.current_url)
    base_element = driver.find_element("id", "card-title")
    assert base_element.is_displayed()


def test_send_code_to_sms(driver):
    """Проверяется отправка кода по смс и редиректа на страницу ввода кода со страница авторизации без пароля"""
    # переходим на страницу
    driver.get(config.elk_url)
    # заполняем поле
    auth_field = driver.find_element("id", "address")
    auth_field.clear()
    auth_field.send_keys(config.phone)

    # нажимаем на кнпоку получить код
    btn_get_code = driver.find_element("id", "otp_get_code")
    btn_get_code.click()
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    base_element = driver.find_element("id", "card-title")
    assert base_element.is_displayed()


def test_move_to_help(driver):
    """Проверяем возможность перехода к странице помощи"""
    # переходим на страницу
    driver.get(config.elk_url)
    # нажимаем на кнопку
    driver.find_element("css selector", "a.rt-link.rt-link--orange.faq-modal-tip__btn").click()
    assert "Ваш безопасный ключ к сервисам Ростелекома" in driver.page_source


def test_block_enter_other_method(driver):
    """Проверяем переход по ссылкам и открытие нужной страницы для бока других методов входа через сторонние сервисы"""
    # переходим на страницу
    driver.get(config.elk_url)
    # нажимаем на кнопки каждого варианта входа и проверяем ссылку
    driver.find_element("id", "oidc_tinkoff").click()
    WebDriverWait(driver, 10).until(lambda x: "https://id.tinkoff.ru/auth" in driver.current_url)
    driver.back()
    driver.find_element("id", "oidc_ya").click()
    # костыль, но почему-то именно эта кнопка не работала с первого раза
    # (руками через браузер не удавалось воспроизвести)
    time.sleep(1)
    driver.find_element("id", "oidc_ya").click()
    WebDriverWait(driver, 10).until(lambda x: "yandex.ru" in driver.current_url)
    driver.back()
    driver.find_element("id", "oidc_vk").click()
    WebDriverWait(driver, 10).until(lambda x: "id.vk.com" in driver.current_url)
    driver.back()
    driver.find_element("id", "oidc_mail").click()
    WebDriverWait(driver, 10).until(lambda x: "mail.ru" in driver.current_url)
    driver.back()
    driver.find_element("id", "oidc_ok").click()
    WebDriverWait(driver, 10).until(lambda x: "connect.ok.ru" in driver.current_url)


def test_move_to_user_agreement(driver):
    """Проверяем переход к пользовательскому соглашению"""
    # переходим на страницу
    driver.get(config.elk_url)
    driver.find_element("id", "rt-auth-agreement-link").click()
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])
    WebDriverWait(driver, 10).until(lambda x: config.agreement_url in driver.current_url)


def test_move_to_forget_password_page(driver):
    """Проверяем переход на страницу восстановления пароля"""
    # переходим на страницу
    driver.get(config.elk_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    # кликаем на кнопку забыл пароль
    driver.find_element("id", "forgot_password").click()
    base_element = driver.find_element("id", "card-title")
    assert base_element.is_displayed()
    assert "Восстановление пароля" in driver.page_source


def test_check_all_auth_variants_elk(driver):
    """Проверяем, что для страницы авторизации на сервис ЕЛК веб присутствует 4 варианта авторизации,
     помимо безпарольных"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    # проверяем нахождение всеx 4 возможных варианта для страницы авторизации
    phone_button = driver.find_element("id", "t-btn-tab-phone")
    mail_button = driver.find_element("id", "t-btn-tab-mail")
    login_button = driver.find_element("id", "t-btn-tab-login")
    ls_button = driver.find_element("id", "t-btn-tab-ls")
    assert phone_button.is_displayed()
    assert mail_button.is_displayed()
    assert login_button.is_displayed()
    assert ls_button.is_displayed()
    # проверяем что по дефолту отображается телефон
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()
    # проверяем кликабельность кнопок и смену полей ввода
    mail_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Электронная почта')]").is_displayed()
    login_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Логин')]").is_displayed()
    ls_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Лицевой счёт')]").is_displayed()
    phone_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()


def test_check_all_auth_variants_onlime(driver):
    """Проверяем, что для страницы авторизации на сервис онлайм присутствует 3 варианта авторизации,
     помимо безпарольных"""
    # переходим на страницу
    driver.get(config.onlime_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # проверяем нахождение всеx 3 возможных варианта для страницы авторизации
    phone_button = driver.find_element("id", "t-btn-tab-phone")
    mail_button = driver.find_element("id", "t-btn-tab-mail")
    login_button = driver.find_element("id", "t-btn-tab-login")
    assert phone_button.is_displayed()
    assert mail_button.is_displayed()
    assert login_button.is_displayed()
    # проверяем что не отображается вариант логина по лицевому счету
    driver.implicitly_wait(1)
    ls_button = driver.find_elements("id", "t-btn-tab-ls")
    if ls_button:
        raise Exception("Отображается вход по лицевому счету на странице")
    # проверяем что по дефолту отображается телефон
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()
    # проверяем кликабельность кнопок и смену полей ввода
    mail_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Электронная почта')]").is_displayed()
    login_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Логин')]").is_displayed()
    phone_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()


def test_check_all_auth_variants_start(driver):
    """Проверяем, что для страницы авторизации на сервис старт веб присутствует 4 варианта авторизации,
     помимо безпарольных"""
    # переходим на страницу
    driver.get(config.start_web_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    # проверяем нахождение всеx 4 возможных варианта для страницы авторизации
    phone_button = driver.find_element("id", "t-btn-tab-phone")
    mail_button = driver.find_element("id", "t-btn-tab-mail")
    login_button = driver.find_element("id", "t-btn-tab-login")
    ls_button = driver.find_element("id", "t-btn-tab-ls")
    assert phone_button.is_displayed()
    assert mail_button.is_displayed()
    assert login_button.is_displayed()
    assert ls_button.is_displayed()
    # проверяем что по дефолту отображается телефон
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()
    # проверяем кликабельность кнопок и смену полей ввода
    mail_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Электронная почта')]").is_displayed()
    login_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Логин')]").is_displayed()
    ls_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Лицевой счёт')]").is_displayed()
    phone_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()


def test_check_all_auth_variants_smart(driver):
    """Проверяем, что для страницы авторизации на сервис смарт присутствует 3 варианта авторизации,
     помимо безпарольных"""
    # переходим на страницу
    driver.get(config.smart_home_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    # проверяем нахождение всеx 3 возможных варианта для страницы авторизации
    phone_button = driver.find_element("id", "t-btn-tab-phone")
    mail_button = driver.find_element("id", "t-btn-tab-mail")
    login_button = driver.find_element("id", "t-btn-tab-login")
    assert phone_button.is_displayed()
    assert mail_button.is_displayed()
    assert login_button.is_displayed()
    # проверяем что не отображается вариант логина по лицевому счету
    driver.implicitly_wait(1)
    ls_button = driver.find_elements("id", "t-btn-tab-ls")
    if ls_button:
        raise Exception("Отображается вход по лицевому счету на странице")
    # проверяем что по дефолту отображается телефон
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()
    # проверяем кликабельность кнопок и смену полей ввода
    mail_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Электронная почта')]").is_displayed()
    login_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Логин')]").is_displayed()
    phone_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()


def test_check_all_auth_variants_key(driver):
    """Проверяем, что для страницы авторизации на сервис ключ присутствует 3 варианта авторизации,
     помимо безпарольных"""
    # переходим на страницу
    driver.get(config.key_web_url)
    WebDriverWait(driver, 10).until(
        lambda x: config.key_web_url in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("xpath", "//div/a[@class='go_kab'][contains(text(), 'Войти')]").click()
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    # проверяем нахождение всеx 3 возможных варианта для страницы авторизации
    phone_button = driver.find_element("id", "t-btn-tab-phone")
    mail_button = driver.find_element("id", "t-btn-tab-mail")
    login_button = driver.find_element("id", "t-btn-tab-login")
    assert phone_button.is_displayed()
    assert mail_button.is_displayed()
    assert login_button.is_displayed()
    # проверяем что не отображается вариант логина по лицевому счету
    driver.implicitly_wait(1)
    ls_button = driver.find_elements("id", "t-btn-tab-ls")
    if ls_button:
        raise Exception("Отображается вход по лицевому счету на странице")
    # проверяем что по дефолту отображается телефон
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()
    # проверяем кликабельность кнопок и смену полей ввода
    mail_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Электронная почта')]").is_displayed()
    login_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Логин')]").is_displayed()
    phone_button.click()
    assert driver.find_element("xpath", "//div/span[contains(text(), 'Мобильный телефон')]").is_displayed()


def test_auth_incorrect_email(driver):
    """Проверяем возможность авторизации с некорректным имейлом"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    # заполянем поле ввода пароля, проверяем обязательность поля имейла
    email_field = driver.find_element("id", "username")
    pass_field = driver.find_element("id", "password")
    pass_field.clear()
    pass_field.send_keys(config.valid_password)
    enter_button = driver.find_element("id", "kc-login")
    enter_button.click()
    assert "https://b2c.passport.rt.ru" in driver.current_url
    assert driver.find_element("id", "username-meta").is_displayed()
    # валидный имейл, но не правильный
    email_field.clear()
    email_field.send_keys(config.random_email)
    enter_button.click()
    assert "https://b2c.passport.rt.ru" in driver.current_url
    # Проверяем сообщение об неправильной паре логина и пароля
    assert driver.find_element("id", "form-error-message").is_displayed()


def test_auth_incorrect_password(driver):
    """Проверяем возможность авторизации с некорректным паролем"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    # заполянем поле ввода пароля, проверяем обязательность поля пароля
    email_field = driver.find_element("id", "username")
    pass_field = driver.find_element("id", "password")
    email_field.clear()
    email_field.send_keys(config.valid_email)
    enter_button = driver.find_element("id", "kc-login")
    enter_button.click()
    assert "https://b2c.passport.rt.ru" in driver.current_url
    # валидный пароль, но не правильный
    pass_field.clear()
    pass_field.send_keys("Fgdhjdj19?")
    enter_button.click()
    assert "https://b2c.passport.rt.ru" in driver.current_url
    # Проверяем сообщение об неправильной паре логина и пароля
    assert driver.find_element("id", "form-error-message").is_displayed()


def test_auth_correct_data(driver):
    """Проверяем возможность авторизации с корректными данными"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопку перехода к странице авторизации по паролю
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    # заполянем поля ввода пароля
    email_field = driver.find_element("id", "username")
    pass_field = driver.find_element("id", "password")
    enter_button = driver.find_element("id", "kc-login")
    email_field.clear()
    email_field.send_keys(config.valid_email)
    pass_field.clear()
    pass_field.send_keys(config.valid_password)
    enter_button.click()
    time.sleep(1)
    # ждем загрузки страницы и сверяем перенаправление на изначальную страницу после авторизации
    WebDriverWait(driver, 10).until(
        lambda x: config.elk_url in driver.current_url)
    # проверяем, что при обновлении страницы происодит автоматическая аутентификация и отсутствует перенаправление
    # на страницу авторизации
    driver.get(config.elk_url)
    assert config.elk_url in driver.current_url


def test_reg_name_validation(driver):
    """Проверяем валидацию поля ввода имени на странице регистрации"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопки для перехода к странице регистрации
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    driver.find_element("id", "kc-register").click()
    driver.implicitly_wait(0.3)
    field = driver.find_element("xpath", "//div/input[@name='firstName']")
    field.clear()

    # чекаем 31 символ
    field.send_keys("Прпвыоывровыорвыоопвылопвыловып")
    base_element = driver.find_element("id", "card-title")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем латиницу
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Googleismuch")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем спец символы
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кир-ил%лиц@а")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем только допустимый спец символ
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("-------------")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем цифру
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кириллица0")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем пробел
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кирил лица")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем 8 символов на кириллице
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кириллиц")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле валидировало невалидные данные"

    # чекаем серединку по количеству символов на кириллице
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Оченьдлинноеимя")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле валидировало невалидные данные"

    # чекаем допустимый спецсимвол
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Корейка-Тянка")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле валидировало невалидные данные"


def test_reg_lastname_validation(driver):
    """Проверяем валидацию поля ввода фамилии на странице регистрации"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопки для перехода к странице регистрации
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    driver.find_element("id", "kc-register").click()
    driver.implicitly_wait(0.3)
    field = driver.find_element("xpath", "//div/input[@name='lastName']")
    field.clear()

    # чекаем 31 символ
    field.send_keys("Прпвыоывровыорвыоопвылопвыловып")
    base_element = driver.find_element("id", "card-title")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем латиницу
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Googleismuch")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем спец символы
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кир-ил%лиц@а")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем только допустимый спец символ
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("-------------")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем цифру
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кириллица0")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем пробел
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кирил лица")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем 8 символов на кириллице
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Кириллиц")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле валидировало невалидные данные"

    # чекаем серединку по количеству символов на кириллице
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Оченьдлинноеимя")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле валидировало невалидные данные"

    # чекаем допустимый спецсимвол
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("Корейка-Тянка")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле валидировало невалидные данные"


def test_reg_phone_email_validation(driver):
    """Проверяем валидацию поля ввода почты/номера на странице регистрации"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопки для перехода к странице регистрации
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    driver.find_element("id", "kc-register").click()
    field = driver.find_element("id", "address")
    field.clear()
    driver.implicitly_wait(0.3)

    # чекаем рандомные числа правильной длины, не с 8/7/9/375
    field.send_keys("56565656565")
    base_element = driver.find_element("id", "card-title")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем рандомные числа не правильной длины, 8/7/9/375
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("565656565")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем рандомные числа не правильной длины, 8/7/9/375
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("123456789012")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем рандомные буквы латиница
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("fdsgldshlksj")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем рандомные буквы кириллица
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("равпыврпдвыолыд")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем рандомные спец символы
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("!№;%:@.,?*")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем не валидную почту
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("kjdfhdlkj@mail")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем не валидную почту
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("ыврпорыв@маил")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем не валидный номер с 8
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("8973723")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем не валидный номер с 7
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("7532626")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем не валидный номер с 375
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("375637")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем не валидный номер с 9
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("97463344343783")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert hint[0].is_displayed(), "Поле валидировало невалидные данные"
    else:
        raise Exception("Поле валидировало невалидные данные")

    # чекаем валидный номер с 8
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("89175663456")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле не валидировало валидные данные"

    # чекаем валидный номер с 7
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("79175663456")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле не валидировало валидные данные"

    # чекаем валидный номер с 9
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("9175663456")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле не валидировало валидные данные"

    # чекаем валидный номер с 375
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("375123456789")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле не валидировало валидные данные"

    # чекаем валидную почту латиница
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys(config.random_email)
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), "Поле не валидировало валидные данные"

    # чекаем валидную почту кириллица
    field.send_keys(Keys.CONTROL + "a", Keys.BACKSPACE)
    base_element.click()
    field.clear()
    field.send_keys("почта@почта.рф")
    base_element.click()
    hint = driver.find_elements("css selector", "span.rt-input-container__meta.rt-input-container__meta--error")
    if hint:
        assert not hint[0].is_displayed(), ("Поле не валидировало валидные данные. Нужны уточнения"
                                            " по поводу использования кириллической почты")


def test_reg_user_case_1(driver):
    """Проверяем валидацию ввод корректных данных во все поля регистрации и переход к следующей странице"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопки для перехода к странице регистрации
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    driver.find_element("id", "kc-register").click()
    name_field = driver.find_element("name", "firstName")
    last_name_field = driver.find_element("name", "lastName")
    mail_field = driver.find_element("id", "address")
    region_btn = driver.find_element("css selector", "input.rt-input__input.rt-select__input.rt-input__input--rounded."
                                                     "rt-input__input--orange")
    pass_field = driver.find_element("name", "password")
    pass_accept_field = driver.find_element("name", "password-confirm")

    # заполняем все поля валидными данными
    name_field.clear()
    name_field.send_keys("Полеимя")
    last_name_field.clear()
    last_name_field.send_keys("Полефамилии")
    mail_field.clear()
    mail_field.send_keys(config.random_email)
    pass_field.clear()
    pass_field.send_keys(config.random_password)
    pass_accept_field.clear()
    pass_accept_field.send_keys(config.random_password)
    region_btn.click()
    regions = driver.find_elements("css selector", "div.rt-select__list-item")
    regions[0].click()
    # нажимаем на кнопку регистрации
    driver.find_element("name", "register").click()
    time.sleep(20)
    assert driver.find_element("id", "card-title").is_displayed()
    assert "https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/registration" in driver.current_url


def test_reg_support(driver):
    """Проверяем возможность перехода на страницу помощи со страницы регистрации"""
    # переходим на страницу
    driver.get(config.elk_url)
    WebDriverWait(driver, 10).until(
        lambda x: "https://b2c.passport.rt.ru/auth/realms/b2c/protocol/openid-connect/auth"
                  in driver.current_url)
    # кликаем на кнопки для перехода к странице регистрации
    driver.find_element("id", "standard_auth_btn").click()
    driver.find_element("id", "t-btn-tab-mail").click()
    driver.find_element("id", "kc-register").click()
    driver.find_element("css selector", "a.rt-link.rt-link--orange.faq-modal-tip__btn").click()
    assert "Ваш безопасный ключ к сервисам Ростелекома" in driver.page_source
