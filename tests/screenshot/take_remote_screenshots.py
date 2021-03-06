import pytest
import json
import requests

# Importing JSON file to get URLs and caps
with open("urls.json", "r") as read_file:
    data = json.load(read_file)

urls = data["urls"]


@pytest.mark.usefixtures('driver')
class TestScreenshots:

    @pytest.mark.parametrize('url', urls)
    def test_screenshots(self, driver, url, browser_config):

        try:        
            r = requests.get(url)
            assert r.status_code != 404
        except:
            pytest.fail(f"Response code is not a 200")

        driver.get(url)

        if 'appiumVersion' in browser_config:
            driver.implicitly_wait(3)

        doc_height = round(int(
            driver.execute_script("return document.body.scrollHeight")))

        # Cutting down device height to prevent overscroll
        device_height = round(int(driver.get_window_size()['height'] / 2))

        # determining number of scrolls
        scroll_amount = round(int(doc_height) / int(device_height))

        scroll = 1

        while scroll < scroll_amount:
            # Gets this via device_height * the number of scroll this is on.
            scroll_y = device_height * scroll

            # Scroll to device_height Y coordinate.
            driver.execute_script(f'window.scrollTo(0,{str(scroll_y)})')

            scroll += 1
