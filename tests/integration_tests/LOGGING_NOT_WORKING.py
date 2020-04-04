""" File that houses all of the integration tests for the Service class """

from service_framework import Service

BASE_DIR = '.'

DO_NOTHING_PATH = f'{BASE_DIR}/data/service_integration_test/do_nothing_service.py'
REPLYER_PATH = f'{BASE_DIR}/data/service_integration_test/replyer_service.py'
REQUESTER_PATH = f'{BASE_DIR}/data/service_integration_test/requester_service.py'

REPLYER_ADDRS = {
    "connections": {
        "in": {
            "reply": {
                "replyer": "127.0.0.1:18900"
            }
        }
    }
}

REQUESTER_ADDRS = {
    "connections": {
        "out": {
            "request": {
                "requester": "127.0.0.1:18900"
            }
        }
    }
}

REQUESTER_CONFIG = {
    'num_req_to_send': 1
}


requester = Service(
    REQUESTER_PATH,
    addresses=REQUESTER_ADDRS,
    config=REQUESTER_CONFIG,
    log_path=f'{BASE_DIR}/logs/requester.log',
    file_loglevel='DEBUG'
)
replyer = Service(
    REPLYER_PATH,
    addresses=REPLYER_ADDRS,
    log_path=f'{BASE_DIR}/logs/replyer.log',
    file_loglevel='DEBUG'
)

replyer.run_service()
requester.run_service()

import time
time.sleep(1)
