""" File used to test the requester - replyer connection pair """

import subprocess
from testing_utils import get_exec_command_for_python_program

RUN_REP_FILE_PATH = './tests/integration_tests/data/main_integration_test/run_replyer.sh'
RUN_REQ_FILE_PATH = './tests/integration_tests/data/main_integration_test/run_request.sh'


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
