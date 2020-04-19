#!/bin/bash

python -m  service_framework \
    -s ./requester_service.py \
    -a ./requester_addresses.json \
    -c ./requester_config.json \
    -cl 'DEBUG' \
    -m
