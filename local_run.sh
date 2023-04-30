#!/bin/bash
# shellcheck shell=bash

PATH_TO_TEST=tests/finance_tests/IO/test_io.py
TEST_CASE_NAME=""
DURATIONS=0
VERBOSE=3

pkill chrome
rm -R allure_reports
if [ "$TEST_CASE_NAME" = "" ]; then
  python -m pytest $PATH_TO_TEST --dist=loadfile -s --verbose --alluredir=allure_reports  --durations=$DURATIONS --verbose -n $VERBOSE
else
  python -m pytest $PATH_TO_TEST::$TEST_CASE_NAME -s --verbose --alluredir=allure_reports
fi
allure serve allure_reports
