#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:../../libs"

export SUB_PORT=8880 # Connect Publishers Here
export PUB_PORT=8881 # Connect Subscribers Here

python main.py -s $SUB_PORT -p $PUB_PORT
