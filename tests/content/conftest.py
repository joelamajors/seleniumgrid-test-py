import pytest
from os import environ
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection
import urllib3

urllib3.disable_warnings()

# Build Name
build_date = datetime.now().strftime('%Y%m%d_%H%M%S')
build_name = f'Google_Tag_Check_{build_date}'


@pytest.fixture(scope='function')
def driver(request):
    browser = {
        "build": build_name,
        "name": "Google Tag Check",
        "platform": "Windows 10",
        "browserName": "Chrome",
        "version": "91.0",
        "console": True,
        "network": True,
        "video": False,
        "headless": True
    }

    desired_caps = {}

    desired_caps.update(browser)

    tunnel_id = environ.get('LT_TUNNEL', False)
    desired_caps['tunnel'] = tunnel_id

    username = environ.get('LT_USERNAME', None)
    access_key = environ.get('LT_ACCESS_KEY', None)
    selenium_endpoint = "http://{}:{}@hub.lambdatest.com/wd/hub".format(
        username, access_key)

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=desired_caps
    )

    yield browser

    if browser is not None:
        print(f'\nLambdaTestSessionID={browser.session_id} '
              + datetime.now().strftime('%H:%M:%S'))
    else:
        raise WebDriverException("Never created!")

    # Teardown starts here
    # report results
    # use the test result to send the pass/fail status to LambdaTest
    result = "failed" if request.node.rep_call.failed else "passed"
    browser.execute_script("lambda-status={}".format(result))
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for LambdaTest reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
