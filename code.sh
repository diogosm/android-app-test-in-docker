#!/bin/bash

TESTS=("test_app_expense")

for TEST in "${TESTS[@]}"
do
  pytest -rA -k $TEST budget_test.py
done
