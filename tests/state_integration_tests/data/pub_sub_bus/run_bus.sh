#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:../../libs"

# -s is SUB_PORT -> Connect Publishers Here
# -p is PUB_PORT -> Connect Subscribers Here

python ./tests/state_integration_tests/data/pub_sub_bus/main.py -s 8880 -p 8881
