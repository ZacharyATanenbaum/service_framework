""" File to house a requester service """

from service_framework import get_logger



def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    LOG = get_logger()

    target_number = config.get('target_number', '12345')
    payload = {'convert_this': target_number}

    LOG.info('Sending payload: %s', payload)
    returned = to_send('request', payload)
    LOG.info('Got converted number: %s', returned['converted'])


config_model = {
    'optional': {
        'target_number': str
    }
}


connection_models = {
    'out': {
        'request': {
            'connection_type': 'requester',
            'required_arguments': {
                'convert_this': str,
            },
            'required_return_arguments': {
                'converted': int
            },
        }
    }
}
