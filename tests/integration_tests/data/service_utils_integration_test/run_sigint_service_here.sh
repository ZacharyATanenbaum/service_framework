#!/bin/bash

python -m  service_framework \
    -s ./sigint_service.py \
    -a ./sigint_addresses.json \
    -cl 'INFO' \
    -m
