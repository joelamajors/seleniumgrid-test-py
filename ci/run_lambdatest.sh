#!/usr/bin/env bash

REMOTE_URL="https://$LT_USERNAME:$LT_ACCESS_KEY@hub.lambdatest.com/wd/hub"

FILTER="tests/test_desktop_scroll_screenshot.py"

pytest $FILTER --remote_url=$REMOTE_URL -n 2
