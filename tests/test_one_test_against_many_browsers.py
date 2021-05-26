import pytest
from pylenium.driver import Pylenium


def search(py, query):
    py.visit('https://google.com')
    py.get('[name="q"]').type(query)
    py.get('[name="btnK"]').submit()
    return py.should().contain_title(query)

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
# browser_targets = py.config.custom['capabilities']['desktop']


@pytest.mark.parametrize('browser', browser_targets)
def test_google_search(py: Pylenium, browser):
    py.config.driver.capabilities.update(browser)
    assert search(py, 'puppies')
