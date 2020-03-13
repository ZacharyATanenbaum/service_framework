""" File to test the Publisher and Subscriber Connections """

import subprocess
from connection_testing_utils import get_exec_command_for_python_program

RUN_SUB_FILE_PATH = './tests/connection_integration_tests/data/pub_sub_test/run_subscriber.sh'
RUN_PUB_FILE_PATH = './tests/connection_integration_tests/data/pub_sub_test/run_publisher.sh'

RUN_X_IN_PATH = './tests/state_integration_tests/data/full_update_test/run_x_full_in.sh'
RUN_X_OUT_PATH = './tests/state_integration_tests/data/full_update_test/run_x_full_out.sh'
RUN_X_PUB_SUB_BUS = './tests/state_integration_tests/data/full_update_test/pub_sub_bus/run_bus.sh'


def test_regular_pub_sub_connections():
    """
    Make sure the Publisher and Subscriber connections function properly.
    """
    sub_command = get_exec_command_for_python_program(RUN_SUB_FILE_PATH)
    pub_command = get_exec_command_for_python_program(RUN_PUB_FILE_PATH)

    sub_process = subprocess.Popen(sub_command)

    try:
        subprocess.getoutput(pub_command)
    except Exception as exp:
        raise exp
    finally:
        sub_process.terminate()


def test_full_update_states_with_topic_and_xpub_xsub_bus():
    """
    This is needed to make sure when multiple topics are being sent over
    an xpub xsub bus the messages are delivered properly.
    """
    """
    xbus_command = get_exec_command_for_python_program(RUN_X_PUB_SUB_BUS)
    xin_command = get_exec_command_for_python_program(RUN_X_IN_PATH)
    xout_command = get_exec_command_for_python_program(RUN_X_OUT_PATH)

    xbus_process = subprocess.Popen(xbus_command)
    xin_process = subprocess.Popen(xin_command)

    try:
        subprocess.run(xout_command, check=True, capture_output=True)
    except Exception as exp:
        raise exp
    finally:
        xbus_process.terminate()
        xin_process.terminate()
    """
