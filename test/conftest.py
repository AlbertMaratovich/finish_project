from selenium import webdriver
import pytest


# start the browser and add waiting and size
@pytest.fixture()
def driver():
    browser = webdriver.Chrome()
    browser.set_window_size(1920, 1080)
    browser.implicitly_wait(10)
    yield browser
    browser.quit()
