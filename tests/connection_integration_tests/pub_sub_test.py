""" File to test the Publisher and Subscriber Connections """

import subprocess
from connection_testing_utils import get_exec_command_for_python_program
from service_framework import get_logger

BASE_DIR = './tests/connection_integration_tests/data/pub_sub_test'
LOG = get_logger()


def test_regular_pub_sub_connections():
    """
    Make sure the Publisher and Subscriber connections function properly.
    """
    run_sub_file_path = f'{BASE_DIR}/regular_pub_sub_connection/run_subscriber.sh'
    run_pub_file_path = f'{BASE_DIR}/regular_pub_sub_connection/run_publisher.sh'

    sub_command = get_exec_command_for_python_program(run_sub_file_path)
    pub_command = get_exec_command_for_python_program(run_pub_file_path)

    sub_process = subprocess.Popen(sub_command)

    try:
        subprocess.getoutput(pub_command)
    except Exception as exp:
        raise exp
    finally:
        sub_process.terminate()


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
