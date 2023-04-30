#!/bin/bash
# shellcheck shell=bash

pkill chrome
CON_NAME=$(docker ps --format "{{.Names}}, {{.Ports}}" | grep "4444")
CONTAINER_NAME=$(echo "$CON_NAME" | cut -d ',' -f 1)
echo "$CONTAINER_NAME"
docker stop "$CONTAINER_NAME"
docker rm "$CONTAINER_NAME"
docker pull selenium/standalone-chrome
docker run -d -p 4444:4444 --name selenium-new selenium/standalone-chrome:latest
CHROME_DRIVER=$(docker exec selenium-new chromedriver --version)
echo "Chrome driver version: ""$CHROME_DRIVER"""
python -m pytest -s --verbose --dist=loadfile --durations=0 -vv -n 4 --reruns 1 --reruns-delay 5 --timeout=1500 --color=yes --junitxml test_results.xml
#python -m pytest tests/test_campaigns.py::test_campaign_duplicate -s --verbose --color=yes --junitxml test_results.xml