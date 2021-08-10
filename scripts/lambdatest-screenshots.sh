#!/bin/bash

# this script will do the following
#  - Download the updated S3 bucket file via AWS CLI
#  - Run the Python command to start the tests

aws s3 cp s3://lambdatest-urls/urls.json /home/ssm-user/scripts/lambdatest-py/urls.json

pytest -s /home/ssm-user/scripts/lambdatest-py/tests/screenshot/take_remote_screenshot.py
