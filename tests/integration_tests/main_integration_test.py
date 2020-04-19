""" File used to test the requester - replyer connection pair """

import os
import subprocess
import time
from service_framework import Service
from testing_utils import get_exec_command_for_python_program


def test_main__main__service_is_directly_runnable():
    """
    Make sure that "python -m service_framework -s service_name.py" still
    functions properly.
    """
    req_command = get_exec_command_for_python_program(RUN_REQ_FILE_PATH)
    rep_command = get_exec_command_for_python_program(RUN_REP_FILE_PATH)

    rep_process = subprocess.Popen(rep_command)

    try:
        req_output = subprocess.run(req_command, check=True, capture_output=True)
    finally:
        rep_process.terminate()

    req_stderr = req_output.stderr.decode('utf-8')
    num_responses = 0

    for line in req_stderr.splitlines():
        if 'Got Response:' in line:
            num_responses += 1

    assert num_responses == 10


def test_main__main__inbound_connections_function_properly():
    """
    Make sure that inbound connections will function correctly in
    main mode.
    """
    outbound = Service(
        OUTBOUND_PATH,
        addresses=OUTBOUND_ADDRS,
        log_path=OUTBOUND_LOG_PATH,
        file_loglevel='DEBUG'
    )
    inbound = Service(
        INBOUND_PATH,
        addresses=INBOUND_ADDRS,
        log_path=INBOUND_LOG_PATH,
        file_loglevel='DEBUG'
    )

    inbound.run_service_as_main()
    outbound.run_service_as_main()

    start = time.time()
    is_success = False

    while not is_success:
        if time.time() - start > 1:
            break

        if not os.path.exists(OUTBOUND_LOG_PATH):
            continue

        with open(INBOUND_LOG_PATH, 'r') as requester_log:
            for line in requester_log.readlines():
                if 'SUCCESS!' in line:
                    is_success = True

    inbound.stop_service() # Make sure to stop service!

    if os.path.exists(INBOUND_LOG_PATH):
        os.remove(INBOUND_LOG_PATH)

    if os.path.exists(OUTBOUND_LOG_PATH):
        os.remove(OUTBOUND_LOG_PATH)

    if not is_success:
        raise RuntimeError('Test failed, figure it out!')


BASE_DIR = './tests/integration_tests'
SERVICE_DIR = f'{BASE_DIR}/data/main_integration_test/inbound_outbound'
LOG_DIR = f'{BASE_DIR}/logs/main_integration_test/inbound_outbound'

RUN_REP_FILE_PATH = f'{BASE_DIR}/data/main_integration_test/run_replyer.sh'
RUN_REQ_FILE_PATH = f'{BASE_DIR}/data/main_integration_test/run_request.sh'
INBOUND_PATH = f'{SERVICE_DIR}/inbound_service.py'
INBOUND_LOG_PATH = f'{LOG_DIR}/inbound_service.log'
OUTBOUND_PATH = f'{SERVICE_DIR}/outbound_service.py'
OUTBOUND_LOG_PATH = f'{LOG_DIR}/outbound_service.log'

INBOUND_ADDRS = {
    "connections": {
        "in": {
            "reply": {
                "replyer": "127.0.0.1:18991"
            }
        }
    }
}

OUTBOUND_ADDRS = {
    "connections": {
        "out": {
            "request": {
                "requester": "127.0.0.1:18991"
            }
        }
    }
}
