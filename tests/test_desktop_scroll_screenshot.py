import os
import pytest
from pylenium.driver import Pylenium



browser_targets = py.config.custom['capabilities']['desktop']
    

def scroll_and_screenshot(py):
    url = py.config.custom['urls'][0]
    py.visit(url)

    page_height = py.get('body').get_attribute('scrollHeight')
    device_height = py.window_size['height'] / 2

    scroll_amount = int(page_height) / int(device_height) - 1

    scroll = 1

    while scroll < scroll_amount:
        file_name = url.strip(
            'https://').replace('.hatfield.marketing', '')
        py.scroll_to(0, device_height)
        py.screenshot(file_name + "/" + file_name + "-" + str(scroll) + '.png')
        device_height += device_height
        scroll += 1
    
    # Stops session
    py.quit()



@pytest.mark.parametrize('browser', browser_targets)
def test_google_search(py: Pylenium, browser):
    py.config.driver.capabilities.update(browser)
    assert search(py, 'puppies')