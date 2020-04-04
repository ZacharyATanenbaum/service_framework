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
    console_loglevel=None,
    file_loglevel='DEBUG'
)
replyer = Service(
    REPLYER_PATH,
    addresses=REPLYER_ADDRS,
    log_path=f'{BASE_DIR}/logs/replyer.log',
    console_loglevel=None
)

replyer.run_service()
import time
time.sleep(0.5)
requester.run_service_as_main()

print('\nSleepy time\b')
time.sleep(1)
print('\nDone Sleepy Time!\n')
