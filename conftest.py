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
with open("urls.json", "r") as read_file:
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
f_caps = open('./caps.json')
caps_data = json.loads(f_caps.read())
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
def driver(request, browser_config):

    desired_caps = dict()
    desired_caps.update(browser_config)

    platform_name = string
    test_name = string

    if "resolution" in browser_config:
        platform_name = browser_config["platform"]
        test_name = f'{platform_name}'\
                    + '_'\
                    + f'{browser_config["browserName"]}'\
                    + '_'\
                    + f'{browser_config["resolution"]}'
    else:
        platform_name = browser_config["deviceName"]
        test_name = f'{platform_name}'\
                    + '_'\
                    + f'{browser_config["platformVersion"]}'\
                    + '_'\
                    + f'{browser_config["appiumVersion"]}'\

    # This needs to be adjusted to use the URL
    build = build_name
    tunnel_id = environ.get('LT_TUNNEL', False)
    username = environ.get('LT_USERNAME', None)
    access_key = environ.get('LT_ACCESS_KEY', None)

    selenium_endpoint = "http://{}:{}@hub.lambdatest.com/wd/hub".format(
        username, access_key)
    desired_caps['build'] = build

    desired_caps['tunnel'] = tunnel_id
    desired_caps['name'] = test_name
    desired_caps['visual'] = True
    desired_caps['network'] = True
    desired_caps['console'] = True

    executor = RemoteConnection(selenium_endpoint, resolve_ip=False)
    browser = webdriver.Remote(
        command_executor=executor,
        desired_capabilities=desired_caps,
        keep_alive=True
    )

    if browser is not None:
        print("\nLambdaTestSessionID={} TestName={} ".format(
            browser.session_id, test_name)
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
