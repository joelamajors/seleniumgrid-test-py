#!/bin/bash

# this script will do the following
#  - Parses AWS key and sets this as environment variables
#  - Downloads the updated urls.json from the S3 bucket via AWS CLI
#  - Run the Python command to start the tests

# Hitting AWS CLI to get the secret value
keys=$(aws secretsmanager get-secret-value --secret-id arn:aws:secretsmanager:us-east-1:838945975189:secret:Lambdatest_QA-VPbu8E --region us-east-1 | jq '.SecretString' | sed -e 's/^"//' -e 's/"$//' | sed -e 's/\\//g')

# Parsing LT_USERNAME and LT_ACCESS_KEY
key_username=$(echo "$keys" | jq -r ".LT_USERNAME")
key_accesskey=$(echo "$keys" | jq -r ".LT_ACCESS_KEY")

# Now set environment variables
export LT_USERNAME="$key_username"
export LT_ACCESS_KEY="$key_accesskey"

cd /home/ssm-user/scripts/lambdatest-py

. ./venv/bin/activate

aws s3 cp s3://lambdatest-urls/urls.json /home/ssm-user/scripts/lambdatest-py/urls.json

pytest -s /home/ssm-user/scripts/lambdatest-py/tests/screenshot/take_remote_screenshots.py