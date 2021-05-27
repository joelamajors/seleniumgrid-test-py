#!/usr/bin/env bash

REMOTE_URL="https://$LT_USERNAME:$LT_ACCESS_KEY@hub.lambdatest.com/wd/hub"

FILTER="tests/test_one_test_against_many_browsers.py"

pytest $FILTER --remote_url=$REMOTE_URL -n 2
