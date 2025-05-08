from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from config import base_url, login, password
import time

driver = webdriver.Chrome()
driver.get(base_url)
driver.set_window_size(1920, 1080)


def test_some():
    return None


