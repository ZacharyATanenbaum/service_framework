""" File to house a requester service """

from logging import getLogger
from service_framework.utils.constants import PACKAGE_LOGGER_NAME

LOG = getLogger(PACKAGE_LOGGER_NAME)


def setup_config(config):
    """
    Make config arguments the proper type!
    """
    config['num_req_to_send'] = int(config['num_req_to_send'])
    return config


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    for num in range(config['num_req_to_send']):
        payload = {'to_echo': 'Hello World - ' + str(num)}

        print('Sending payload: ... ')

        LOG.info('Sending payload: %s', payload)
        returned = to_send('request', payload)

        LOG.info('Got Response: %s', returned)


config_model = {
    'required': {
        'num_req_to_send': int,
    }
}


connection_models = {
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
