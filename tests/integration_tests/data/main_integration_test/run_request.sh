#!/bin/bash

python -m  service_framework -s  ./tests/integration_tests/data/main_integration_test/requester_service.py -a  ./tests/integration_tests/data/main_integration_test/requester_addresses.json -m num_req_to_send 10
