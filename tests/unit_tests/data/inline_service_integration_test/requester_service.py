""" File to house a requester service """

from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def setup_config(config):
    """
    Make config arguments the proper type!
    """
    LOG.info('Setting up config!')
    config['num_req_to_send'] = int(config.get('num_req_to_send', 2))
    return config


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    for num in range(config['num_req_to_send']):
        payload = {'to_echo': 'Hello World - ' + str(num)}

        LOG.info('Sending payload: %s', payload)
        returned = to_send('request', payload)
        LOG.info('Got Response: %s', returned)

    LOG.info('GOT ALL RESPONSES')


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
