import string
import pytest
from os import environ
import json
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection
import urllib3

urllib3.disable_warnings()

# Importing JSON file to get URLs and caps
with open("./urls.json", "r") as read_file:
    data = json.load(read_file)

urls = data["urls"]
# Returns first URL to parse build_name
check_url = urls[0]

now = datetime

# Build Name
site_name = check_url.replace("https://", '')\
                     .replace("http://", '')\
                     .split("/")[0]\
                     .split(".")
build_date = datetime.now().strftime('%Y%m%d_%H%M%S')

build_name = f'{site_name[0]}_{build_date}'

# Importing capabilities
with open("./caps.json") as read_caps:
    caps_data = json.load(read_caps)

browsers = []
browsers.extend(caps_data["caps"]["desktop"])
browsers.extend(caps_data["caps"]["mobile"])


def pytest_generate_tests(metafunc):
    if 'driver' in metafunc.fixturenames:
        metafunc.parametrize(
            'browser_config',
            browsers,
            ids=_generate_param_ids(
                'broswerConfig',
                browsers
            ),
            scope='function')


def _generate_param_ids(name, values):
    return [("<%s:%s>" % (name, value)).replace('.', '_') for value in values]


@pytest.fixture(scope='function')
def driver(request, browser_config, url):
    desired_caps = dict()
    desired_caps.update(browser_config)

    # This needs to be adjusted to use the URL
    tunnel_id = environ.get('LT_TUNNEL', False)
    username = environ.get('LT_USERNAME', None)
    access_key = environ.get('LT_ACCESS_KEY', None)

    selenium_endpoint = "http://{}:{}@hub.lambdatest.com/wd/hub".format(
        username, access_key)

    build = build_name
    desired_caps['name'] = url
    desired_caps['build'] = build
    desired_caps['tunnel'] = tunnel_id
    desired_caps['visual'] = True
    desired_caps['network'] = True
    desired_caps['console'] = True

    print(desired_caps)

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=desired_caps,
        keep_alive=True
    )

    if browser is not None:
        print(f'\nLambdaTestSessionID={browser.session_id} '
                + datetime.now().strftime('%H:%M:%S'))
    else:
        raise WebDriverException("Never created!")

    yield browser
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
