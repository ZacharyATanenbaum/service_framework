""" File to house integration tests for the service utils """

import os
import time
import uuid
import pytest
from service_framework import Service
from service_framework.utils import service_utils, utils


def test_service_utils__setup_service_connections__no_connection_models_case():
    """
    Make sure if there's no connection models then an empty dict is returned.
    """
    imported_service = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    config = {}
    conns = service_utils.setup_service_connections(ADDRESSES_PATH, imported_service, config)
    assert conns == {}


def test_service_utils__setup_service_connections__connection_models_case():
    """
    Make sure if there are connection models they are properly loaded.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    conns = service_utils.setup_service_connections(addresses, imported_service, config)
    conn = conns['in']['in_connection_1']
    assert conn.__class__.__name__ == 'Replyer'


def test_service_utils__setup_service_connections__connection_models_and_setup_conn_models_case():
    """
    Make sure setup_service_connections is properly called.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    conns = service_utils.setup_service_connections(addresses, imported_service, config)
    conn = conns['out']['out_connection_1']
    assert conn.__class__.__name__ == 'Requester'


def test_service_utils__setup_to_send__valid_connection_output_type_for_to_send():
    """
    Make sure that sending will function if the output type is a connection
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(connections, {})

    out_connection = connections['out']['out_connection_1']
    out_connection.args_validator = lambda args: None
    out_connection.send = lambda payload: RETURN_PAYLOAD
    to_send('out_connection_1', {})


def test_service_utils__setup_to_send__args_are_put_into_to_send_payload():
    """
    Make sure arguments are actually put into the payload
    """
    def check_payload(payload):
        """
        This function is used to validate send payloads have the passed
        arguments
        """
        if payload['args'] != PROPER_ARGS:
            raise RuntimeError('Payload does not have args added!!!')

        return RETURN_PAYLOAD

    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(connections, {})

    connections['out']['out_connection_1'].send = check_payload
    to_send('out_connection_1', PROPER_ARGS)


def test_service_utils__setup_to_send__workflow_id_put_into_to_send_payload():
    """
    Make sure if a workflow id is provided it is added to the payload.
    """
    workflow_id = uuid.uuid4()

    def check_payload(payload):
        """
        This function is used to validate send payloads have the passed
        arguments
        """
        assert payload['workflow_id'] == workflow_id
        return RETURN_PAYLOAD

    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(
        connections,
        {},
        workflow_id=workflow_id,
        increment_id=True
    )

    connections['out']['out_connection_1'].send = check_payload
    to_send('out_connection_1', PROPER_ARGS)


def test_service_utils_setup_to_send__workflow_id_incremented_on_to_send_calls():
    """
    Make sure the workflow id appends the call number increases with each to_send
    call. This will allow a developer to more easily debug later down the line.
    """
    workflow_id = uuid.uuid4()
    call_count = 0

    def check_payload(payload):
        """
        This function is used to validate send payloads have the passed
        arguments
        """
        nonlocal call_count

        if call_count == 0:
            assert payload['workflow_id'] == workflow_id

        else:
            new_workflow_id = '{}_{}'.format(workflow_id, call_count)
            assert payload['workflow_id'] == new_workflow_id

        call_count += 1
        return RETURN_PAYLOAD

    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(
        connections,
        {},
        workflow_id=workflow_id,
        increment_id=True
    )

    connections['out']['out_connection_1'].send = check_payload

    for _ in range(4):
        to_send('out_connection_1', PROPER_ARGS)


def test_service_utils_setup_to_send__workflow_id_constant_on_to_send_calls():
    """
    Make sure the workflow id does not increment when "increment_id" is False.
    This will allow services that are in main_mode to not increment the same
    uuid consistently.
    """
    workflow_id = uuid.uuid4()

    def check_payload(payload):
        """
        This function is used to validate send payloads have the passed
        arguments
        """
        assert payload['workflow_id'] == workflow_id
        return RETURN_PAYLOAD

    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(
        connections,
        {},
        workflow_id=workflow_id,
        increment_id=False
    )

    connections['out']['out_connection_1'].send = check_payload

    for _ in range(4):
        to_send('out_connection_1', PROPER_ARGS)



def test_service_utils__setup_to_send__to_send_validates_args_case():
    """
    Make sure that to_send validates passed arguments.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(connections, {})

    connections['out']['out_connection_1'].send = lambda payload: None

    with pytest.raises(ValueError):
        to_send('out_connection_1', {})


def test_service_utils__setup_to_send__to_send_validates_returned_args_case():
    """
    Make sure that the return arguments case will also be validated.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(connections, {})

    connections['out']['out_connection_1'].send = lambda payload: None

    with pytest.raises(ValueError):
        to_send('out_connection_1', PROPER_ARGS)


def test_service_utils__setup_to_send__to_send_returns_proper_args():
    """
    Make sure the to_send function properly sends arguments and
    gets the returned arguments back.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_service_connections(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(connections, {})

    connections['out']['out_connection_1'].send = lambda payload: RETURN_PAYLOAD
    return_arguments = to_send('out_connection_1', PROPER_ARGS)

    assert return_arguments == RETURN_PAYLOAD['return_args']


def test_service_utils__run_init_function__init_function_runs_properly():
    """
    Make sure the init function will run properly
    """
    requester = Service(
        REQUESTER_PATH,
        addresses=REQUESTER_ADDRS,
        config=REQUESTER_CONFIG,
        log_path=REQUESTER_LOG_PATH,
        file_loglevel='DEBUG'
    )
    replyer = Service(
        REPLYER_PATH,
        addresses=REPLYER_ADDRS,
        log_path=REPLYER_LOG_PATH,
        file_loglevel='DEBUG'
    )

    replyer.run_service()
    requester.run_service_as_main()

    start = time.time()
    is_success = False

    while not is_success:
        if time.time() - start > 1:
            break

        if not os.path.exists(REQUESTER_LOG_PATH):
            continue

        with open(REQUESTER_LOG_PATH, 'r') as requester_log:
            for line in requester_log.readlines():
                if 'GOT ALL RESPONSES' in line:
                    is_success = True

    replyer.stop_service() # Make sure to stop service!

    if os.path.exists(REQUESTER_LOG_PATH):
        os.remove(REQUESTER_LOG_PATH)

    if os.path.exists(REPLYER_LOG_PATH):
        os.remove(REPLYER_LOG_PATH)

    if not is_success:
        raise RuntimeError('Test failed, figure it out!')


BASE_DIR = './tests/integration_tests'
BASE_DATA_DIR = f'{BASE_DIR}/data/service_utils_integration_test'
BASE_LOG_DIR = f'{BASE_DIR}/logs/service_utils_integration_test'

ADDRESSES_PATH = f'{BASE_DATA_DIR}/addresses.json'
SERVICE_PATH = f'{BASE_DATA_DIR}/service.py'
WO_SERVICE_PATH = f'{BASE_DATA_DIR}/wo_service.py'
MAIN_SERVICE_PATH = f'{BASE_DATA_DIR}/main_service.py'

PROPER_ARGS = {'this_is_a_test_arg': 'Test Value!'}
RETURN_PAYLOAD = {
    'return_args': {
        'this_is_a_return_arg': 'ReturnArgHi!',
    },
}

REPLYER_PATH = f'{BASE_DATA_DIR}/run_init_function/replyer_service.py'
REPLYER_LOG_PATH = f'{BASE_LOG_DIR}/run_init_function/replyer_service.log'
REQUESTER_PATH = f'{BASE_DATA_DIR}/run_init_function/requester_service.py'
REQUESTER_LOG_PATH = f'{BASE_LOG_DIR}/run_init_function/requester_service.log'

REPLYER_ADDRS = {
    "in": {
        "reply": {
            "replyer": "127.0.0.1:12222"
        }
    }
}

REQUESTER_ADDRS = {
    "out": {
        "request": {
            "requester": "127.0.0.1:12222"
        }
    }
}

REQUESTER_CONFIG = {
    'num_req_to_send': 2
}
