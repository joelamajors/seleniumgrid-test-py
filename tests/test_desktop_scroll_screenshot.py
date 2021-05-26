import os
import pytest
from pylenium.driver import Pylenium


base_url = 'https://ntg.hatfield.marketing'


def scroll_and_screenshot(py):
    py.visit(base_url)

    page_height = py.get('body').get_attribute('scrollHeight')
    device_height = py.window_size['height'] / 2

    scroll_amount = int(page_height) / int(device_height) - 1

    scroll = 1

    while scroll < scroll_amount:
        file_name = base_url.strip(
            'https://').replace('.hatfield.marketing', '')
        py.scroll_to(0, device_height)
        py.screenshot(file_name + "/" + file_name + "-" + str(scroll) + '.png')
        device_height += device_height
        scroll += 1
