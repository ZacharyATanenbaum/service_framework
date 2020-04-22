""" File that houses all of the integration tests for the Service class """

import os
import time
from service_framework import Service, get_logger

LOG = get_logger()


def test_service__init__service_can_be_constructed_with_just_service_path():
    """
    Make sure the only thing the Service Class needs is a service_path.
    """
    do_nothing_path = f'{BASE_SERVICE_DIR}/do_nothing_service.py'
    service = Service(do_nothing_path)
    service.run_service()
    service.stop_service() # Make sure to stop service!


def test_service__services_can_be_run_programmatically_via_importing():
    """
    Make sure the file loglevel and log folder function properly.
    """
    requester_log_path = f'{BASE_LOG_DIR}/service_can_be_run_programmatically/requester.log'
    replyer_log_path = f'{BASE_LOG_DIR}/service_can_be_run_programmatically/replyer.log'

    requester_addresses = {**REQUESTER_ADDRS}
    requester_addresses['connections']['out']['request']['requester'] = '127.0.0.1:18777'

    replyer_addresses = {**REPLYER_ADDRS}
    replyer_addresses['connections']['in']['reply']['replyer'] = '127.0.0.1:18777'

    replyer_path = f'{BASE_SERVICE_DIR}/replyer_service.py'
    requester_path = f'{BASE_SERVICE_DIR}/requester_service.py'

    requester = Service(
        requester_path,
        addresses=requester_addresses,
        config=REQUESTER_CONFIG,
        log_path=requester_log_path,
        file_loglevel='DEBUG'
    )
    replyer = Service(
        replyer_path,
        addresses=replyer_addresses,
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


def test_service__services_can_be_run_as_classess():
    """
    Make sure the file loglevel and log folder function properly when
    passing classes into the Service object instead of a path to be imported.
    """
    requester_log_path = f'{BASE_LOG_DIR}/service_can_be_run_as_classes/requester.log'
    replyer_log_path = f'{BASE_LOG_DIR}/service_can_be_run_as_classes/replyer.log'

    requester_addresses = {**REQUESTER_ADDRS}
    requester_addresses['connections']['out']['request']['requester'] = '127.0.0.1:18666'

    replyer_addresses = {**REPLYER_ADDRS}
    replyer_addresses['connections']['in']['reply']['replyer'] = '127.0.0.1:18666'

    requester_obj = RequesterClass()
    replyer_obj = ReplyerClass()

    requester = Service(
        service_obj=requester_obj,
        addresses=requester_addresses,
        config=REQUESTER_CONFIG,
        log_path=requester_log_path,
        file_loglevel='DEBUG'
    )
    replyer = Service(
        service_obj=replyer_obj,
        addresses=replyer_addresses,
        log_path=replyer_log_path,
        file_loglevel='DEBUG',
        console_loglevel='DEBUG'
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
BASE_LOG_DIR = f'{BASE_DIR}/logs/service_integration_test'
BASE_SERVICE_DIR = f'{BASE_DIR}/data/service_integration_test'


REPLYER_ADDRS = {
    "connections": {
        "in": {
            "reply": {
                "replyer": "overwrite_this"
            }
        }
    }
}

REQUESTER_ADDRS = {
    "connections": {
        "out": {
            "request": {
                "requester": "overwrite_this"
            }
        }
    }
}

REQUESTER_CONFIG = {
    'num_req_to_send': 2
}


class RequesterClass:
    def setup_config(self, config):
        """
        Make config arguments the proper type!
        """
        LOG.info('Setting up config!')
        config['num_req_to_send'] = int(config['num_req_to_send'])
        return config


    def main(self, to_send, config):
        """
        This function is the main entrance into the Requester Service
        """
        for num in range(config['num_req_to_send']):
            payload = {'to_echo': 'Hello World - ' + str(num)}

            LOG.info('Sending payload: %s', payload)
            returned = to_send(
                'connection',
                'request',
                payload
            )

            LOG.info('Got Response: %s', returned)

        LOG.info('GOT ALL RESPONSES')

    def __init__(self):
        self.config_model = {
            'required': {
                'num_req_to_send': int,
            }
        }

        self.connection_models = {
            'out': {
                'request': {
                    'connection_type': 'requester',
                    'required_arguments': {
                        'to_echo': str,
                    },
                    'required_return_arguments': {
                        'echoed': str,
                    }
                }
            }
        }


class ReplyerClass:
    def on_new_request(self, args, to_send, states, config):
        """
        Method triggered when a new request is recieved from
        a requester.
        """
        LOG.info('Got payload: %s', args)
        response = {'echoed': args['to_echo']}
        LOG.info('Responding with: %s', response)
        return response

    def __init__(self):
        self.connection_models = {
            'in': {
                'reply': {
                    'connection_type': 'replyer',
                    'required_creation_arguments': {
                        'on_new_request': self.on_new_request,
                    },
                    'required_arguments': {
                        'to_echo': str,
                    },
                    'required_return_arguments': {
                        'echoed': str,
                    }
                }
            }
        }
