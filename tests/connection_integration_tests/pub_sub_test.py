""" File to test the Publisher and Subscriber Connections """

import subprocess
from connection_testing_utils import get_exec_command_for_python_program

BASE_DIR = './tests/connection_integration_tests/data/pub_sub_test'
RUN_X_PUB_SUB_BUS = './tests/state_integration_tests/data/pub_sub_bus/run_bus.sh'


def test_regular_pub_sub_connections():
    """
    Make sure the Publisher and Subscriber connections function properly.
    """
    run_sub_file_path = f'{BASE_DIR}/run_subscriber.sh'
    run_pub_file_path = f'{BASE_DIR}/run_publisher.sh'

    sub_command = get_exec_command_for_python_program(run_sub_file_path)
    pub_command = get_exec_command_for_python_program(run_pub_file_path)

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
    run_x_in_path = f'{BASE_DIR}/run_x_full_in.sh'
    run_x_out_path = f'{BASE_DIR}/run_x_full_out.sh'

    xbus_command = get_exec_command_for_python_program(RUN_X_PUB_SUB_BUS)
    xin_command = get_exec_command_for_python_program(run_x_in_path)
    xout_command = get_exec_command_for_python_program(run_x_out_path)

    xbus_process = subprocess.Popen(xbus_command)
    xin_process = subprocess.Popen(xin_command)

    try:
        subprocess.run(xout_command, check=True, capture_output=True)
    except Exception as exp:
        raise exp
    finally:
        xbus_process.terminate()
        xin_process.terminate()


def test_connector_pub_binder_sub():
    """
    Make sure that the publisher can be the connector and the subscriber
    can be the binder for a many to one relationship.
    """
    run_sub_file_path = f'{BASE_DIR}/connector_pub_binder_sub/run_subscriber.sh'
    run_pub_file_path = f'{BASE_DIR}/connector_pub_binder_sub/run_publisher.sh'

    sub_command = get_exec_command_for_python_program(run_sub_file_path)
    pub_command = get_exec_command_for_python_program(run_pub_file_path)

    sub_process = subprocess.Popen(sub_command)

    try:
        subprocess.getoutput(pub_command)
    except Exception as exp:
        raise exp
    finally:
        sub_process.terminate()
