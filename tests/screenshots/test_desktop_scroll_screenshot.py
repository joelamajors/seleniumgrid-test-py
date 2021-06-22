import pytest
import json
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection



# Importing JSON file to get URLs and caps
with open("./pylenium.json", "r") as capabilities:
    caps = json.load(capabilities)

urls = caps["custom"]["urls"]
browser_targets = caps["custom"]["capabilities"]["desktop"]


def get_url(driver, url):
    driver.get(url)


# Scrolls and takes a screenshot.
# May change depending on how we want to retreive the screenshots in AWS
def scroll_and_screenshot(driver,
                          url,
                          browser_name,
                          browser_version,
                          browser_platform,
                          browser_resolution):

    # added conditional for URL
    if "https" in driver.getCurrentUrl():
        page_name = url.strip('https://').replace(
                    '.hatfield.marketing', '').rstrip("/").split("/")
    else:
        page_name = url.strip('http://').replace(
                    '.hatfield.marketing', '').rstrip("/").split("/")

    # Parse the returned page_name to see if this contains any slashes.
    # Get the last one
    page_name_int = len(page_name) - 1
    page_name = page_name[page_name_int]

    # Height of the whole page
    page_height = round(int(driver.find_element_by_tag_name('body').get_attribute('scrollHeight')))

    # Cutting device height in half so there's not over scroll
    device_height = round(int(py.window_size['height'] / 2))

    # Number of scrolls
    scroll_amount = round(int(page_height) / int(device_height))

    scroll = 1

    while scroll < scroll_amount:
        # Scroll to device_height Y coordinate.
        # Gets this via device_height * the number of scroll this is on.
        py.scroll_to(0, (device_height * scroll))

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

    print(f'CURRENT BROWSER:\\\
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
