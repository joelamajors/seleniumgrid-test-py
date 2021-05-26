#!/usr/bin/env bash

REMOTE_URL="https://$LT_USERNAME:$LT_ACCESS_KEY@hub.lambdatest.com/wd/hub"

FILTER="tests/test_screenshot_desktop.py"

echo $LT_USERNAME
echo $LT_ACCESS_KEY

pytest $FILTER --remote_url=$REMOTE_URL
