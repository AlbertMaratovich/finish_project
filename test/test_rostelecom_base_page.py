from selenium import webdriver
from selenium.webdriver import ActionChains
import config
import locators
import time

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.implicitly_wait(10)


def test_buttons_header():
    """Открытие главной страницы и проверка перехода по всем вкладкам хедера, кроме оплаты, которая будет
    проверена отдельно"""
    driver.get(config.base_url)

    # find landind button and click on it
    driver.find_element("css selector", locators.l_landing_btn).click()
    # check the url
    assert driver.current_url == config.base_url

    # find btn for me and click
    driver.find_element("xpath", locators.l_for_me_btn).click()
    # check the url
    assert driver.current_url == config.base_url

    # find btn for business and click
    driver.find_element("xpath", locators.l_for_business).click()
    # check the url
    assert driver.current_url == config.business_url

    # find btn for operators and click
    driver.back()
    driver.find_element("xpath", locators.l_for_operators).click()
    # check the url
    assert driver.current_url == config.operators_url

    # find btn blog and click
    driver.back()
    driver.find_element("xpath", locators.l_for_blog_btn).click()
    # check the url
    assert driver.current_url == config.blog_url

    # find drop button and click
    driver.back()
    driver.find_element("css selector", locators.l_drop_btn).click()
    # click on about company button
    driver.find_element("xpath", locators.l_about_company).click()
    # check the url
    assert driver.current_url == config.about_company_url

    # find drop button and click
    driver.back()
    driver.find_element("css selector", locators.l_drop_btn).click()
    # click on for partners button
    driver.find_element("xpath", locators.l_for_partners).click()
    # check the url
    assert driver.current_url == config.for_partners_url

    # find drop button and click
    driver.back()
    driver.find_element("css selector", locators.l_drop_btn).click()
    # click on for investors button
    driver.find_element("xpath", locators.l_for_investors).click()
    # check the url
    assert driver.current_url == config.for_investors_url

    # find btn blog and click
    driver.back()
    driver.find_element("xpath", locators.l_games_btn).click()
    # check the url
    assert driver.current_url == config.games_url

    # find btn blog and click
    driver.back()
    driver.find_element("xpath", locators.l_bonuses_btn).click()
    # check the url
    assert driver.current_url == config.bonuses_url

    # find btn blog and click
    driver.back()
    driver.find_element("xpath", locators.l_help_btn).click()
    # check the url
    assert driver.current_url == config.help_url


def test_move_to_payment_page_from_header():
    """Переход с главной страницы на страницу оплаты при помощи кнопок хедера"""
    driver.get(config.base_url)
    # find drop button and click
    driver.find_element("css selector", locators.l_payment_btn).click()
    # click on for rostelecom payment button
    driver.find_element("xpath", locators.l_payment_rostelecom).click()
    # check the url and 404 status
    assert driver.current_url == config.payment_page_url
    if config.error_not_found_text in driver.page_source:
        raise Exception("Status - 404 Not Found")

    # find drop button and click
    driver.back()
    driver.find_element("css selector", locators.l_payment_btn).click()
    # click on for other organizations button
    driver.find_element("xpath", locators.l_other_organizations).click()
    # check the url and 404 status
    assert driver.current_url == config.payment_other_organizations_url
    """Понимаю, что метод достаточно колхозный для обнаружения ошибки 404, думаю что при проектирвоании тестов я бы
        проверял наличии каких-то главных элементов на странице. По сколько страница падает в ошибку я не могу заранее
        определить такой элемент (открывается заглушка для 404), а статус код при помощи селениума проверить нельзя"""
    if config.error_not_found_text in driver.page_source:
        raise Exception("Status - 404 Not Found")

    # find drop button and click
    driver.back()
    driver.find_element("css selector", locators.l_payment_btn).click()
    # click on find payment button
    driver.find_element("xpath", locators.l_find_payment).click()
    # check the url and 404 status
    assert driver.current_url == config.find_payment_url
    if config.error_not_found_text in driver.page_source:
        raise Exception("Status - 404 Not Found")


def test_load_page_payment_for_other():
    """Проверка загрузки и отображения страницы оплаты для других организаций с тела сайта"""
    driver.get(config.base_url)
    # find button
    btn_other_org_body = driver.find_element("css selector", locators.l_other_org_body)
    # scroll to btn
    action = ActionChains(driver).scroll_to_element(btn_other_org_body)
    action.perform()
    # find other organization button and click
    time.sleep(0.5)
    btn_other_org_body.click()
    # move to new handle
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])
    # check the url
    assert driver.current_url == "https://payment.rt.ru/rt/provider"
    if config.error_not_found_text in driver.page_source:
        raise Exception("Status - 404 Not Found")


def test_load_page_payment_find_payment():
    """Проверка загрузки и отображение элементов страницы поиска оплаты с тела сайта"""
    driver.get(config.base_url)
    # find button
    btn_find_payment_body = driver.find_element("css selector", locators.l_find_payment_body)
    # scroll to btn
    action = ActionChains(driver).scroll_to_element(btn_find_payment_body)
    action.perform()
    # find search payment button and click
    time.sleep(0.5)
    btn_find_payment_body.click()
    # move to new handle
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])
    # check the url
    assert driver.current_url == config.find_payment_url
    if config.error_not_found_text in driver.page_source:
        raise Exception("Status - 404 Not Found")


def test_move_to_payment_page():
    """Проверка ввода корректных данных в поля быстрой оплаты услуг ростелекома и перехода к странице оплаты"""
    driver.get(config.base_url)
    # find button
    bunner = driver.find_element("css selector", "div.rt-col div.checkup-banner__block.sp-v-orange")
    btn_move_to_payment = driver.find_element("xpath", locators.l_move_to_pay_btn)
    # scroll to btn
    action = ActionChains(driver).scroll_to_element(bunner)
    action.perform()
    time.sleep(0.5)
    # find and add keys to fields
    field_personal_account = driver.find_element("xpath", locators.l_personal_account_field)
    field_personal_account.clear()
    field_personal_account.send_keys("6666666")
    field_amount = driver.find_element("xpath", locators.l_amount_field)
    field_amount.clear()
    field_amount.send_keys("10000")

    btn_move_to_payment.click()
    # move to new handle
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])
    # check the url
    assert config.payment_page_url in driver.current_url
    if config.error_not_found_text in driver.page_source:
        raise Exception("Status - 404 Not Found")
