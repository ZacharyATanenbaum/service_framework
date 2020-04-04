""" File to house a requester service """

from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


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
        returned = to_send(
            'connection',
            'request',
            payload
        )

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
