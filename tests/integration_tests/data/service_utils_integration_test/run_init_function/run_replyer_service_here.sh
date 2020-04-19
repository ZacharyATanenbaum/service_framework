#!/bin/bash

python -m  service_framework \
    -s ./replyer_service.py \
    -a ./replyer_addresses.json \
    -cl 'DEBUG'
