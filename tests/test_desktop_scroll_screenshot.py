import os
import pytest
from selenium import webdriver
from pylenium.driver import Pylenium


@pytest.fixture
def selenium():
    username = os.getenv('LT_USERNAME')
    access_key = os.getenv('LT_ACCESS_KEY')
    remote_url = 'https://{};{}@hub.lambdatest.com/wd/hub'.format(username,access_key)

    desired_caps = {
        "build": "Pyleniumio test",
        "name": "Pyleniumio test case", 
        "platform": "Windows 10", 
        "browserName": "Chrome",
        "version": "89.0",
        "user": username,
        'accessKey': access_key
    }

    driver = webdriver.Remote(
        command_executor=remote_url,
        desired_capabilities=desired_caps
    )

    yield driver
    driver.quit()
    

base_url = 'https://ntg.hatfield.marketing'

# def test_desktop_scroll_screenshot(py):
#     py.visit(base_url)
#     py.find('.footer-hatfield-links')

#     window_height = py.window_size['height']

#     scroll_length = window_height

    # py.scroll_to(0, scroll_length)

    # py.screenshot()


def test_screen_height(py: Pylenium):
    py.visit(base_url)
    file = open('ntg_test', 'w+')
    window_height = py.window_size['height']
    file.write(str(window_height))

