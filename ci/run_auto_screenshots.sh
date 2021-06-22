#!/usr/bin/env bash

https://api.lambdatest.com/screenshots/v1/

REMOTE_URL="https://$LT_USERNAME:$LT_ACCESS_KEY@hub.lambdatest.com/wd/hub"

FILTER="tests/screenshots/test_desktop_scroll_local_screenshot.py"

pytest $FILTER --remote_url=$REMOTE_URL -s
