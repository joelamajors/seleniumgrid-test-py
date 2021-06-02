import os
import os.path
from os import path
from _pytest import config
import pytest
from pylenium.driver import Pylenium
import json




# Importing JSON file to get URLs and caps
f = open('./pylenium.json')
data = json.loads(f.read())
urls = data["custom"]["urls"]
device_targets = data["custom"]["capabilities"]["mobile"]


def get_url(py, url):
    py.visit(url)

# Scrolls and takes a screenshot. This might changes depending on how we want to retreive the screenshots once in AWS
def scroll_and_screenshot(py, url, device_name, device_type, device_platform, appium_version):

    # Height of the whole page
    page_height = round(int(py.get('body').get_attribute('scrollHeight')))

    # Cutting device height in half so there's not over scroll
    device_height = round(int(py.window_size['height'] / 2))

    # Number of scrolls
    scroll_amount = round(int(page_height) / int(device_height))

    scroll = 1  

    # added conditional for URL
    if "https" in py.url(): 
        page_name = url.strip('https://').replace('.hatfield.marketing', '').rstrip("/").split("/")
    else:
        page_name = url.strip('http://').replace('.hatfield.marketing', '').rstrip("/").split("/")

    # # Generates site name, used for saving screenshots
    site_name = page_name[0]

    # # Parse the returned page_name to see if this contains any slashes. Get the last one
    page_name_int = len(page_name) - 1
    page_name = page_name[page_name_int]
    
    while scroll < scroll_amount:

        # Scroll to device_height Y coordinate. Gets this via device_height * the number of scroll this is on. 
        py.scroll_to(0, (device_height*scroll))

        # device_height += device_height
        scroll += 1


@pytest.mark.parametrize('url', urls)
@pytest.mark.parametrize('device', device_targets)
def test_scroll_down_on_page(py: Pylenium, url, device):
    py.config.driver.capabilities.update(device)

    device_name = device["platformName"]
    device_type = device["deviceName"]
    device_platform = device["platformVersion"]
    appium_version = device["appiumVersion"]

    print(f'\nCurrent Browser:\nDevice Name: {device_name}\nDevice Type: {device_type}\nPlatform Version: {device_platform}\nAppium Version: {appium_version}\nURL: {url}')
    get_url(py, url)

    scroll_and_screenshot(py, url, device_name, device_type, device_platform, appium_version)