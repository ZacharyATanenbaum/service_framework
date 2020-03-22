""" File used to test the requester - replyer connection pair """

import subprocess
from connection_testing_utils import get_exec_command_for_python_program

RUN_FILE_PATH = './tests/connection_integration_tests/data/external_request/run_external_request.sh'


def test_external_request_happy_case():
    """
    Make sure that an external request will be properly conducted.
    """
    run_command = get_exec_command_for_python_program(RUN_FILE_PATH)
    output = subprocess.run(run_command, check=False, capture_output=True)
    output_stderr = output.stderr.decode('utf-8')

    successful = False
    for line in output_stderr.splitlines():
        if 'SUCCESS_HITTING_EXTERNAL_SERVICE' in line:
            successful = True

    if not successful:
        print(output_stderr)
        raise RuntimeError('Failed to properly hit external service. Figure it out!')
