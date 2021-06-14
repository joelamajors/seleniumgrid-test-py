import pytest
import sys
import os
import os.path
from os import path
from _pytest import config
import json

# Importing JSON file to get URLs and caps
f = open('./urls.json')
data = json.loads(f.read())
urls = data["urls"]

@pytest.mark.usefixtures('driver')
class TestScreenshots:

    @pytest.mark.parametrize('url', urls)
    def test_screenshots(self, driver, url):
        """
        Go to page and scroll down
        :return: None
        """
        driver.get(url)
        
        # Assigning page_name variable
        name = None

        # Needs to change if we're testing a non dev URL
        if "https" in driver.current_url:
            name = url.strip('https://').rstrip("/").split(".")
        else:
            name = url.strip('http://').rstrip("/").split(".")

        # Parse the returned page_name to see if this contains any slashes.
        # Get the last one

        page_names = name[len(name)-1].split('/')
        page_name = page_names[len(page_names)-1]
    
        # Height of the whole document
        document_height = round(int(driver.execute_script("return document.body.scrollHeight")))

        # Cutting device height in half so there's not over scroll
        device_height = round(int(driver.get_window_size()['height'] / 2))

        # Number of scrolls
        scroll_amount = round(int(document_height) / int(device_height))

        scroll = 1

        while scroll < scroll_amount:
            # Scroll to device_height Y coordinate.
            # Gets this via device_height * the number of scroll this is on.
            scroll_y = device_height * scroll

            driver.execute_script("window.scrollTo(0, " + str(scroll_y) + ")")

            scroll += 1