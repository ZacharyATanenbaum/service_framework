#!/bin/bash

python -m  service_framework -s  ./tests/connection_integration_tests/data/request_replyer_test/requester_service.py -a  ./tests/connection_integration_tests/data/request_replyer_test/requester_addresses.json -m num_req_to_send 10
