""" File to house a requester service """

from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def setup_config(config):
    """
    Make config arguments the proper type!
    """
    LOG.info('Setting up config!')
    config['num_req_to_send'] = int(config['num_req_to_send'])
    return config


def init_function(to_send, config):
    """
    Call this function prior to starting the service
    """
    LOG.info('Init Function was called!')

    for num in range(config['num_req_to_send']):
        payload = {'to_echo': 'Hello World - ' + str(num)}

        LOG.info('Sending payload: %s', payload)
        returned = to_send('request', payload)

        LOG.info('Got Response: %s', returned)

    LOG.info('GOT ALL RESPONSES')


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    LOG.info('RUNNING THAT MAIN THANG')


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
