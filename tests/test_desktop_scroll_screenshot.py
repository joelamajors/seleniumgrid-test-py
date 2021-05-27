import os
import os.path
from os import path
import pytest
from pylenium.driver import Pylenium

browser_targets = [
    {
        "platform": "Windows 10",
        "browserName": "Chrome",
        "version": "89.0",
        "resolution": "1366x768"
    },
    {
        "platform": "MacOS Bigsur",
        "browserName": "Safari",
        "version": "14.0",
        "resolution": "1440x900"
    }
]


def scroll_and_screenshot(py):
    url = 'https://ntg.hatfield.marketing'
    py.visit(url)

    page_height = py.get('body').get_attribute('scrollHeight')
    device_height = py.window_size['height'] / 2

    scroll_amount = int(page_height) / int(device_height) - 1

    scroll = 1

    file_name = url.strip('https://').replace('.hatfield.marketing', '')

    if not path.isdir(file_name):
        os.mkdir(file_name)

    while scroll < scroll_amount:
        py.screenshot(file_name + "/" + file_name + "-" + str(scroll) + '.png')
        py.scroll_to(0, device_height)
        device_height += device_height
        scroll += 1

    # Stops session
    py.quit()


@pytest.mark.parametrize('browser', browser_targets)
def test_scroll_and_screenshot(py: Pylenium, browser):
    py.config.driver.capabilities.update(browser)
    assert scroll_and_screenshot(py)
