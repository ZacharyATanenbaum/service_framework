""" File that houses all of the integration tests for the Service class """

import os
import time
from service_framework import Service


def test_service__init__service_can_be_constructed_with_just_service_path():
    """
    Make sure the only thing the Service Class needs is a service_path.
    """
    service = Service(DO_NOTHING_PATH)
    service.run_service()
    service.stop_service() # Make sure to stop service!


def test_service__services_can_be_run_programmatically():
    """
    Make sure the file loglevel and log folder function properly.
    """
    requester_log_path = f'{BASE_LOG_DIR}/requester.log'
    replyer_log_path = f'{BASE_LOG_DIR}/replyer.log'

    requester = Service(
        REQUESTER_PATH,
        addresses=REQUESTER_ADDRS,
        config=REQUESTER_CONFIG,
        log_path=requester_log_path,
        file_loglevel='DEBUG'
    )
    replyer = Service(
        REPLYER_PATH,
        addresses=REPLYER_ADDRS,
        log_path=replyer_log_path,
        file_loglevel='DEBUG'
    )

    replyer.run_service()
    requester.run_service_as_main()

    start = time.time()
    is_success = False

    while not is_success:
        if time.time() - start > 1:
            break

        if not os.path.exists(requester_log_path):
            continue

        with open(requester_log_path, 'r') as requester_log:
            for line in requester_log.readlines():
                if 'GOT ALL RESPONSES' in line:
                    is_success = True

    replyer.stop_service() # Make sure to stop service!

    if os.path.exists(requester_log_path):
        os.remove(requester_log_path)

    if os.path.exists(replyer_log_path):
        os.remove(replyer_log_path)

    if not is_success:
        raise RuntimeError('Test failed, figure it out!')


BASE_DIR = './tests/integration_tests'
BASE_LOG_DIR = f'{BASE_DIR}/logs/service_integration_test/service_can_be_run_programmatically'

DO_NOTHING_PATH = f'{BASE_DIR}/data/service_integration_test/do_nothing_service.py'
REPLYER_PATH = f'{BASE_DIR}/data/service_integration_test/replyer_service.py'
REQUESTER_PATH = f'{BASE_DIR}/data/service_integration_test/requester_service.py'

REPLYER_ADDRS = {
    "connections": {
        "in": {
            "reply": {
                "replyer": "127.0.0.1:18777"
            }
        }
    }
}

REQUESTER_ADDRS = {
    "connections": {
        "out": {
            "request": {
                "requester": "127.0.0.1:18777"
            }
        }
    }
}

REQUESTER_CONFIG = {
    'num_req_to_send': 2
}
