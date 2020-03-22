#!/bin/bash

python -m  service_framework -s  ./tests/connection_integration_tests/data/external_request/external_request_service.py -cl 'DEBUG' -m --product_id 'BTC-USD'
