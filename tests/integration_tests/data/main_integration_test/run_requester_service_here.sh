#!/bin/bash

python -m  service_framework -s  ./requester_service.py -a  ./requester_addresses.json -m num_req_to_send 10
