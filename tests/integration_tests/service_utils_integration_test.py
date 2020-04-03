""" File to house integration tests for the service utils """

import logging
import signal
import subprocess
import time
import uuid
import pytest
import zmq
from service_framework.utils import msgpack_utils, service_utils, socket_utils, utils
import testing_utils

LOG = logging.getLogger(__name__)

ADDRESSES_PATH = './tests/integration_tests/data/service_utils_integration_test/addresses.json'
SERVICE_PATH = './tests/integration_tests/data/service_utils_integration_test/service.py'
WO_SERVICE_PATH = './tests/integration_tests/data/service_utils_integration_test/wo_service.py'
MAIN_SERVICE_PATH = './tests/integration_tests/data/service_utils_integration_test/main_service.py'
SIGINT_PATH = './tests/integration_tests/data/service_utils_integration_test/run_sigint_service.sh'
PROPER_ARGS = {'this_is_a_test_arg': 'Test Value!'}
RETURN_PAYLOAD = {
    'return_args': {
        'this_is_a_return_arg': 'ReturnArgHi!',
    },
}


def test_service_utils__setup_connections__no_connection_models_case():
    """
    Make sure if there's no connection models then an empty dict is returned.
    """
    imported_service = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    config = {}
    conns = service_utils.setup_connections(ADDRESSES_PATH, imported_service, config)
    assert conns == {}


def test_service_utils__setup_connections__connection_models_case():
    """
    Make sure if there are connection models they are properly loaded.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    conns = service_utils.setup_connections(addresses, imported_service, config)
    conn = conns['in']['in_connection_1']
    assert conn.__class__.__name__ == 'Replyer'


def test_service_utils__setup_connections__connection_models_and_setup_conn_models_case():
    """
    Make sure setup_connections is properly called.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    conns = service_utils.setup_connections(addresses, imported_service, config)
    conn = conns['out']['out_connection_1']
    assert conn.__class__.__name__ == 'Requester'


def test_service_utils__setup_states__state_models_case():
    """
    Make sure setup_states actually works properly.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    state = states['in']['in_state_1']
    assert state.__class__.__name__ == 'FullUpdateIn'


def test_service_utils__setup_states__state_models_and_setup_state_models_case():
    """
    Make sure setup_state_models actually works properly...
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    state = states['out']['out_state_1']
    assert state.__class__.__name__ == 'FullUpdateOut'


def test_service_utils__setup_to_send__invalid_output_type_for_to_send():
    """
    Make sure to_send will not send if the output type is not 'connection' or
    'state'
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(states, connections, {})
    args = {'this_is_a_test_field': 'Hi'}

    with pytest.raises(ValueError):
        to_send('banana', 'out_state_1', args)


def test_service_utils__setup_to_send__valid_connection_output_type_for_to_send():
    """
    Make sure that both sending will function if the output type is a connection
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(states, connections, {})

    out_connection = connections['out']['out_connection_1']
    out_connection.args_validator = lambda args: None
    out_connection.send = lambda payload: RETURN_PAYLOAD
    to_send('connection', 'out_connection_1', {})


def test_service_utils__setup_to_send__valid_state_output_type_for_to_send():
    """
    Make sure that both sending will function if the output type is a state
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(states, connections, {})

    out_state = states['out']['out_state_1']
    out_state.args_validator = lambda args: None
    out_state.send = lambda payload: None
    to_send('state', 'out_state_1', {})


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
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(states, connections, {})

    connections['out']['out_connection_1'].send = check_payload
    to_send('connection', 'out_connection_1', PROPER_ARGS)


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
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(
        states,
        connections,
        {},
        workflow_id=workflow_id,
        increment_id=True
    )

    connections['out']['out_connection_1'].send = check_payload
    to_send('connection', 'out_connection_1', PROPER_ARGS)


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
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(
        states,
        connections,
        {},
        workflow_id=workflow_id,
        increment_id=True
    )

    connections['out']['out_connection_1'].send = check_payload

    for _ in range(4):
        to_send('connection', 'out_connection_1', PROPER_ARGS)


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
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(
        states,
        connections,
        {},
        workflow_id=workflow_id,
        increment_id=False
    )

    connections['out']['out_connection_1'].send = check_payload

    for _ in range(4):
        to_send('connection', 'out_connection_1', PROPER_ARGS)



def test_service_utils__setup_to_send__to_send_validates_args_case():
    """
    Make sure that to_send validates passed arguments.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(states, connections, {})

    connections['out']['out_connection_1'].send = lambda payload: None

    with pytest.raises(ValueError):
        to_send('connection', 'out_connection_1', {})


def test_service_utils__setup_to_send__to_send_validates_returned_args_case():
    """
    Make sure that the return arguments case will also be validated.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(states, connections, {})

    connections['out']['out_connection_1'].send = lambda payload: None

    with pytest.raises(ValueError):
        to_send('connection', 'out_connection_1', PROPER_ARGS)


def test_service_utils__setup_to_send__to_send_returns_proper_args():
    """
    Make sure the to_send function properly sends arguments and
    gets the returned arguments back.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    to_send = service_utils.setup_to_send(states, connections, {})

    connections['out']['out_connection_1'].send = lambda payload: RETURN_PAYLOAD
    return_arguments = to_send('connection', 'out_connection_1', PROPER_ARGS)

    assert return_arguments == RETURN_PAYLOAD['return_args']


def test_service_utils__run_main__connection_in_will_error():
    """
    Explicitly state that inbound connections will not function
    if using the main_mode of the service framework.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)

    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    conns = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    main_func = lambda to_send, config: True

    with pytest.raises(ValueError):
        service_utils.run_main(config, conns, states, main_func, {})


def test_service_utils__run_main__main_runs_successfully():
    """
    Test that the service_framework main mode will run a "hello world"
    main method.
    """
    imported_service = utils.import_python_file_from_cwd(MAIN_SERVICE_PATH)

    config = {}
    cur_addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addresses = service_utils.setup_addresses(cur_addresses, imported_service, config)
    conns = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)
    main_func = lambda to_send, config: True

    service_utils.run_main(config, conns, states, main_func, {})


def test_service_utils__setup_sigint_handler_func__sucessfully_called_custom_sigint_handler():
    """
    Test if the service_framework will properly call a custom sigint handler function on
    sigint.
    """
    LOG.info('Creating Subscriber Socket')
    context = zmq.Context()
    sub_socket = socket_utils.get_subscriber_socket('127.0.0.1:7007', context)

    LOG.info('Running Server')
    run_command = testing_utils.get_exec_command_for_python_program(SIGINT_PATH)
    process = subprocess.Popen(run_command)

    time.sleep(0.35) # Yeah, I know this isn't great. It's an integration test okay?
    LOG.info('Running Kill Command')
    process.send_signal(signal.SIGINT)

    # If no SIGINT 1 then something wrong with main call...
    payload1 = msgpack_utils.msg_unpack(sub_socket.recv())
    LOG.info('Got payload 1: %s', payload1)

    # If no SIGINT 2 then something wrong with sigint_handler call...
    payload2 = msgpack_utils.msg_unpack(sub_socket.recv())
    LOG.info('Got payload 2: %s', payload2)

    assert payload1['args']['message'] == 'handler1'
    assert payload2['args']['message'] == 'handler2'
