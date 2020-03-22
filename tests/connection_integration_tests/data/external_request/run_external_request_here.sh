#!/bin/bash

python -m  service_framework \
    -s  ./external_request_service.py \
    -cl 'DEBUG' \
    -m \
    --product_id 'BTC-USD'
