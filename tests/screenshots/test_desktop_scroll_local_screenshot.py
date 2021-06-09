import pytest
from pylenium.driver import Pylenium
import json
import os
from os import path


with open("./pylenium.json", "r") as caps:
    caps_loaded = json.load(caps)

# Importing JSON file to get URLs and caps
f = open('./pylenium.json')
data = json.loads(f.read())
urls = data["custom"]["urls"]
browser_targets = data["custom"]["capabilities"]["desktop"]


def get_url(py, url):
    py.visit(url)


def scroll_and_screenshot(py,
                          url,
                          browser_name,
                          browser_version,
                          browser_platform,
                          browser_resolution):

    # added conditional for URL
    if "https" in py.url():
        page_name = url.replace('https://', '').replace(
                    '.hatfield.marketing', '').rstrip("/").split("/")
    else:
        page_name = url.replace('http://', '').replace(
                    '.hatfield.marketing', '').rstrip("/").split("/")

    # Parse the returned page_name to see if this contains any slashes.
    # Get the last one
    page_name_int = len(page_name) - 1
    page_name = page_name[page_name_int]

    # ~~~ setup path for method of saving tests ~~~
    full_path = f'screenshots/desktop/{page_name}/{browser_platform}/{browser_name}_{browser_version}'

    # Making file name
    file_name = f'{browser_name}_{browser_resolution}'

    # If the path does not exist, make one
    if not path.isdir(full_path):
        os.makedirs(full_path)

    # Getting base screenshot before scrolling
    py.screenshot(f'{full_path}/{file_name}_0_base.png')

    # getting full page height for later scrolling
    full_page_height = round(int(py.get('body').get_attribute('scrollHeight')))

    # Cutting device height in half so there's not over scroll
    device_height = round(int(py.window_size['height'] * .7))

    # Number of scrolls
    scroll_amount = round(int(full_page_height) / int(device_height))

    scroll = 1

    while scroll < scroll_amount:
        # Scroll to device_height Y coordinate.
        # Gets this via device_height * the number of scroll this is on.
        py.scroll_to(0, (device_height * scroll))

        py.screenshot(f'{full_path}/{file_name}_{str(scroll)}.png')

        scroll += 1


@pytest.mark.parametrize('url', urls)
@pytest.mark.parametrize('browser', browser_targets)
def test_scroll_down_on_page(py: Pylenium, url, browser):
    py.config.driver.capabilities.update(browser)
    print('\n')
    print(f'CURRENT URL: {url}')

    browser_name = browser["browserName"]
    browser_version = browser["version"]
    browser_platform = browser["platform"]
    browser_resolution = browser["resolution"]

    print(f'CURRENT BROWSER:\
            \n{browser_name},\
            \n{browser_version},\
            \n{browser_platform},\
            \n{browser_resolution}')

    get_url(py, url)

    scroll_and_screenshot(py,
                          url,
                          browser_name,
                          browser_version,
                          browser_platform,
                          browser_resolution)
