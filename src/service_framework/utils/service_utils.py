""" File to house service utility functions """

import json
import logging
import threading
import uuid
import zmq
from service_framework.utils import (
    connection_utils,
    logging_utils,
    socket_utils,
    state_utils,
    utils,
    validation_utils
)

LOG = logging.getLogger(__name__)
RUN_FLAG = True


def get_all_new_payloads(polling_list, poller):
    """
    polling_list = [{
        'inbound_socket': zmq.Context.Socket,
        'decode_message': def(bytes) -> payload,
        'args_validator': def(args),
        'connection_function': def(args) -> args or None,
        'model_function': def(args, to_send, states, conifg) -> return_args or None,
        'return_validator': def(return_args)
        'return_function': def(return_args),
    }]
    poller::zmq.Poller
    """
    payloads = []

    for idx, item in enumerate(polling_list):
        polled_socket = dict(poller.poll(idx))
        current_socket = item['inbound_socket']

        if not current_socket in polled_socket:
            payloads.append(None)
            continue

        if polled_socket[current_socket] != zmq.POLLIN:
            LOG.debug('Current socket from item "%s" not zmq.POLLIN!', item)
            payload.append(None)
            continue

        binary_message = current_socket.recv()
        payload = item['decode_message'](binary_message)
        payloads.append(payload)

    return payloads


def get_current_states(states):
    """
    states = {
        'in': {
            'state_name': BaseState(),
        },
        'out': {
            'state_name': BaseState(),
        },
    }
    return = {
        'in': {
           'in_state_name': {},
        },
        'out': {
           'out_state_name': {},
        },
    }
    """
    if 'in' in states:
        return {
            state_name: state.get_state()
            for state_name, state in states['in'].items()
        }
    return {}


def get_polling_list(connections, states):
    """
    connections = {
        'in': {
            'connection_name': BaseConnector(),
        },
        'out': {
            'connection_name': BaseConnector(),
        },
    }
    states = {
        'in': {
            'state_name': BaseState(),
        },
        'out': {
            'state_name': BaseState(),
        },
    }
    return::[{
        'inbound_socket': zmq.Context.Socket,
        'decode_message': def(bytes) -> payload,
        'args_validator': def(args),
        'connection_function': def(args) -> args or None,
        'model_function': def(args, to_send, states, conifg) -> return_args or None,
        'return_validator': def(return_args)
        'return_function': def(return_args),
    }]
    """
    LOG.info('Getting all sockets and function from states and connections.')
    polling_list = []

    for side in ('in', 'out'):
        LOG.debug('Getting all sockets and functions from side: %s', side)

        if side in connections:
            for connection_name, connection in connections[side].items():
                LOG.debug('Getting all sockets and function from %s', connection_name)
                polling_list += connection.get_inbound_sockets_and_triggered_functions()

        if side in states:
            for state_name, state in states[side].items():
                LOG.debug('Getting all sockets and functions from %s', state_name)
                polling_list += state.get_inbound_sockets_and_triggered_functions()

    LOG.info('Got %s sockets and functions!', len(polling_list))
    return polling_list


def run_main(service_path, addresses, config, logger_args_dict):
    """
    This is used to run a program that will be on the leading edge of a
    Python Service Framework graph or a program that will not respond to
    events.
    service_path = './services/other_folder/service_file.py'
    addresses = {
        'connections' {
            'in': {
                'connection_name': {
                    'socket_name': str
                },
            },
            'out': {},
        },
        'states': {}
    }
    config = {
        'config_1': 'thingy',
        'config_2': 12345
    }
    logger_args_dict = {
        console_loglevel: str,
        log_path: str,
        file_loglevel: str,
        backup_count: int,
    }
    """
    logging_utils.setup_package_logger(**logger_args_dict)

    imported_service = utils.import_python_file_from_cwd(service_path)
    config = setup_config(config, imported_service)
    addresses = setup_addresses(addresses, imported_service, config)
    connections = setup_connections(addresses, imported_service, config)
    states = setup_states(addresses, imported_service, config)

    setup_sigint_handler_func(
        imported_service,
        config,
        connections,
        states,
        logger_args_dict
    )

    if 'in' in connections and connections['in']:
        raise ValueError('In connections do not work in main_mode. Please remove.')

    if 'in' in states and states['in']:
        raise ValueError('In states do not work in main_mode. Please remove.')

    to_send = setup_to_send(
        states,
        connections,
        logger_args_dict,
        workflow_id=None,
        increment_id=False
    )

    service_thread = threading.Thread(
        target=run_service,
        args=(config, connections, states, logger_args_dict)
    )

    def sigint_handler(signum, _):
        LOG.info('Got SIGINT "%s"! Cleaning up...', signum)
        global RUN_FLAG
        RUN_FLAG = False

    utils.add_sigint_handler(sigint_handler)
    service_thread.daemon = True
    service_thread.start()

    imported_service.main(to_send, config)
    global RUN_FLAG
    RUN_FLAG = False # Not needed, but makes tests run much faster


def run_service(service_path, addresses, config, logger_args_dict):
    """
    service_path = './services/other_folder/service_file.py'
    addresses = {
        'connections' {
            'in': {
                'connection_name': {
                    'socket_name': str
                },
            },
            'out': {},
        },
        'states': {}
    }
    config = {
        'config_1': 'thingy',
        'config_2': 12345
    }
    logger_args_dict = {
        console_loglevel: str,
        log_path: str,
        file_loglevel: str,
        backup_count: int,
    }
    """
    logging_utils.setup_package_logger(**logger_args_dict)

    imported_service = utils.import_python_file_from_cwd(service_path)
    config = setup_config(config, imported_service)
    addresses = setup_addresses(addresses, imported_service, config)
    connections = setup_connections(addresses, imported_service, config)
    states = setup_states(addresses, imported_service, config)

    setup_sigint_handler_func(
        imported_service,
        config,
        connections,
        states,
        logger_args_dict
    )

    polling_list = get_polling_list(connections, states)
    sockets = [item['inbound_socket'] for item in polling_list]
    poller = socket_utils.get_poller_socket(sockets)

    LOG.debug('Starting Service Loop...')

    global RUN_FLAG
    while RUN_FLAG:
        payloads = get_all_new_payloads(polling_list, poller)

        for idx, payload in enumerate(payloads):
            if payload is None:
                continue

            LOG.debug('Got Payload: %s', payload)
            args = payload.get('args')
            workflow_id = payload.get('workflow_id')

            logging_utils.set_new_workflow_id_on_logger(workflow_id, logger_args_dict)
            current_polled = polling_list[idx]
            LOG.debug('Polled item: %s', current_polled)

            LOG.debug('Validating Args for the model function: %s', args)
            if current_polled.get('args_validator', None):
                current_polled['args_validator'](args)

            LOG.debug('Running Connection/State Function (if applicable)')
            post_func = current_polled.get('connection_function', None)
            post_func = current_polled.get('state_function', post_func)
            args = args if post_func is None else post_func(args)
            LOG.debug('Finished Running Connection/State Function args: %s', args)

            return_args = args
            if current_polled.get('model_function', None):
                to_send = setup_to_send(
                    states,
                    connections,
                    logger_args_dict,
                    workflow_id=workflow_id,
                    increment_id=True
                )

                return_args = current_polled['model_function'](
                    args,
                    to_send,
                    get_current_states(states),
                    config
                )

            if current_polled.get('return_function', None):
                if current_polled.get('return_validator', None):
                    LOG.debug('Validating Returned Args: %s', return_args)
                    current_polled['return_validator'](return_args)

                current_polled['return_function']({
                    'return_args': return_args,
                    'workflow_id': payload.get('workflow_id'),
                })

            logging_utils.set_new_workflow_id_on_logger(None, logger_args_dict)


def setup_addresses(addresses, imported_service, config):
    """
    addrs_path::str Relative import path to the addresses file
    imported_service::module The imported service python file
    return = {
        'connections': {
            'in': {
                'connection_name': {
                    'socket_name_1': '127.0.0.1:5001',
                    'socket_name_2': '127.0.0.1:5002',
                },
            },
            'out': {
                'connection_name': {
                    'socket_name_1': '256.24.52.1:9000',
                },
            },
        },
        'states': {},
    }
    config = {
        'config_key_1': 'config_val_1'
    }
    """
    if not addresses:
        return addresses

    if hasattr(imported_service, 'setup_addresses'):
        LOG.info('Found "setup_addresses" in service, Calling now...')
        addresses = imported_service.setup_addresses(addresses, config)

        if not isinstance(addresses, dict):
            err = 'setup_addresses function must return a dict of addresses!'
            LOG.error(err)
            raise ValueError(err)

    return addresses


def setup_config(config, imported_service):
    """
    config::{} Config that has already been parsed
    imported_service::module The imported service python file
    return::{} ex. {**file_arguments, 'random_argument': 'HELLO'}
    """
    if not hasattr(imported_service, 'config_model') and config:
        err = 'Must provide a "config_model" func in the service if using a config.'
        LOG.error(err)
        raise ValueError(err)

    if not hasattr(imported_service, 'config_model'):
        LOG.warning('No "config_model" in Service File. Skipping config setup...')
        return {}

    LOG.info('Found "config_model", Setting up Config...')

    if hasattr(imported_service, 'setup_config'):
        LOG.info('Found "setup_config" Function, Calling now...')
        config = imported_service.setup_config(config)

        if not isinstance(config, dict):
            err = 'setup_config function must return a dict of configs!'
            LOG.error(err)
            raise ValueError(err)

    validation_utils.validate_args(
        config,
        imported_service.config_model.get('required', {}),
        imported_service.config_model.get('optional', {})
    )

    return config


def setup_connections(addresses, imported_service, config):
    """
    addresses = {
        'connections': {
            'in': {
                'connection_name': {
                    'socket_name_1': '127.0.0.1:5001',
                    'socket_name_2': '127.0.0.1:5002',
                },
            },
            'out': {
                'connection_name': {
                    'socket_name_1': '256.24.52.1:9000',
                },
            },
        },
        'states': {},
    }
    imported_service::module The imported service python file
    return = {
        'in': {
            'connection_name': BaseInConnector(),
        }
        'out': {
            'connection_name': BaseOutConnector(),
        },
    }
    config = {
        'config_key_1': 'config_val_1'
    }
    """
    if not hasattr(imported_service, 'connection_models'):
        LOG.warning('No "connection_models" in Service File! Skipping connection setup...')
        return {}

    LOG.info('Found "connection_models", Setting up Connections...')
    connection_models = imported_service.connection_models

    if hasattr(imported_service, 'setup_connection_models'):
        LOG.info('Found "setup_connection_models", Calling now...')
        connection_models = imported_service.setup_connection_models(
            connection_models,
            config
        )

        if not isinstance(connection_models, dict):
            err = 'setup_connection_models function must return a dict of models!'
            LOG.error(err)
            raise ValueError(err)

    return connection_utils.setup_connections(
        connection_models,
        addresses
    )


def setup_to_send(states, connections, logger_args_dict, workflow_id=None, increment_id=True):
    """
    Setup the function that the service will call to make external calls.
    states = {
        'in': {
            'state_name': BaseState(),
        },
        'out': {
            'state_name': BaseState(),
        },
    },
    connections = {
        'in': {
            'connection_name': BaseConnector(),
        },
        'out': {
            'connection_name': BaseConnector(),
        },
    }
    logger_args_dict = {
        console_loglevel: str,
        log_folder: None,
        file_loglevel: str,
        backup_count: int,
    }
    workflow_id::str
    increment_id::bool
    return def(output_type, output_name, args)
    """
    local_state = {
        'num_calls': 0,
        'workflow_id': uuid.uuid4() if not workflow_id and increment_id else workflow_id,
    }

    def get_output(output_type, output_name):
        """
        output_type::set('state', 'connection')
        output_name::str Either the state or connections name
        return StateObject or ConnectionObject
        """
        outputs = connections if output_type == 'connection' else states
        return outputs['out'][output_name]

    def get_current_workflow_id():
        """
        Update the current workflow id based on the number of calls done by
        the service.
        """
        cur_workflow_id = local_state['workflow_id']
        cur_workflow_id = cur_workflow_id if cur_workflow_id else uuid.uuid4()

        if local_state['num_calls'] > 0:
            cur_workflow_id = '{}_{}'.format(cur_workflow_id, local_state['num_calls'])

        if increment_id:
            local_state['num_calls'] += 1

        return cur_workflow_id

    def create_out_payload(args, cur_workflow_id):
        """
        Method to create the proper payload prior to sending the payload.
        Mainly used to increment the workflow id for multiple branching
        calls.
        args::{}
        return::{}
        """
        return {
            'args': args,
            'workflow_id': cur_workflow_id
        }

    def parse_out_response(response):
        """
        Method to set state parse response after sending the payload.
        response::{}
        return::{}
        """
        if response is None:
            return {}
        return response.get('return_args')

    def to_send(output_type, output_name, args):
        """
        Used to wrap external service calls for testing/documentation/readability.
        Needs to be a function so when it's passed to the model function the
        end user can simply call this function. Without having to do additional
        instantiations.
        output_type::set('state', 'connection')
        output_name::str Either the state or connections name
        args::{} Arguments to pass to the state/connectionn
        """
        cur_workflow_id = get_current_workflow_id()
        logging_utils.set_new_workflow_id_on_logger(cur_workflow_id, logger_args_dict)

        LOG.debug(
            'Sending to output_type %s output_name %s args %s',
            output_type,
            output_name,
            args
        )

        if output_type not in ('state', 'connection'):
            error = 'Output type for to_send must be "state" or "connection"!'
            LOG.error(error)
            raise ValueError(error)

        output_to = get_output(output_type, output_name)

        LOG.debug('Checking args to send')
        output_to.args_validator(args)

        LOG.debug('Creating payload to send')
        payload = create_out_payload(args, cur_workflow_id)

        LOG.debug('Sending payload: %s', payload)
        response = output_to.send(payload)

        LOG.debug('Parsing returned Response: %s', response)
        returned_args = parse_out_response(response)

        LOG.debug('Validating response from send function')
        output_to.return_validator(returned_args)

        LOG.debug('Returning Response arguments: %s', returned_args)
        logging_utils.set_new_workflow_id_on_logger(None, logger_args_dict)

        return returned_args

    return to_send


def setup_states(addresses, imported_service, config):
    """
    addresses = {
        'connections': {
            'in': {
                'connection_name': {
                    'socket_name_1': '127.0.0.1:5001',
                    'socket_name_2': '127.0.0.1:5002',
                },
            },
            'out': {
                'connection_name': {
                    'socket_name_1': '256.24.52.1:9000',
                },
            },
        },
        'states': {},
    }
    imported_service::module The imported service python file
    return = {
        'in': {
            'state_name': BaseInState(),
        },
        'out': {
            'state_name': BaseOutState(),
        },
    }
    config = {
        'config_key_1': 'config_val_1',
    }
    """
    if not hasattr(imported_service, 'state_models'):
        LOG.warning('No "state_model" in Service File. Skipping state setup...')
        return {}

    LOG.info('Found "state_models", Setting up States...')
    state_models = imported_service.state_models

    if hasattr(imported_service, 'setup_state_models'):
        LOG.info('Found "setup_state_models", Calling now...')
        state_models = imported_service.setup_state_models(state_models, config)

        if not isinstance(state_models, dict):
            err = 'setup_state_models function must return a dict of state models!'
            LOG.error(err)
            raise ValueError(err)

    return state_utils.setup_states(state_models, addresses)


def setup_sigint_handler_func(imported_service, config, connections, states, logger_args_dict):
    """
    This function is used to setup a custom sigint handler provided from
    the imported service.
    imported_service::module The imported service python file
    config = {'config_arg_1': 'config_value_1', ...}
    connections = {
        'in': {
            'connection_name': BaseConnector(),
        },
        'out': {
            'connection_name': BaseConnector(),
        },
    }
    states = {
        'in': {
            'state_name': BaseState(),
        },
        'out': {
            'state_name': BaseState(),
        },
    }
    logger_args_dict = {
        console_loglevel: str,
        log_folder: None,
        file_loglevel: str,
        backup_count: int,
    }
    """
    if not hasattr(imported_service, 'sigint_handler'):
        LOG.warning('No "sigint_handler" in Service File. Skipping Sigint setup...')
        return

    LOG.info('Found "sigint_handler! Setting up now...')
    to_send = setup_to_send(
        states,
        connections,
        logger_args_dict
    )

    def custom_sigint_handler(sigint, frame):
        imported_service.sigint_handler(
            sigint,
            frame,
            to_send,
            get_current_states(states),
            config
        )

    utils.add_sigint_handler(custom_sigint_handler)
