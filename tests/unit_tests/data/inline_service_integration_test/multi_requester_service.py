""" File to house a requester service """

from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def setup_config(config):
    """
    Make config arguments the proper type!
    """
    LOG.info('Setting up config!')
    config['num_req_to_send'] = int(config.get('num_req_to_send', 2))
    config['responses_recieved'] = []
    return config


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    for num in range(config['num_req_to_send']):
        payload = {'to_echo': 'Hello World - ' + str(num)}

        LOG.info('Sending payload to request_1: %s', payload)
        returned = to_send('request_1', payload)
        LOG.info('Got Response from request_1: %s', returned)
        config['responses_recieved'].append(returned)

        LOG.info('Sending payload to request_2: %s', payload)
        returned = to_send('request_2', payload)
        LOG.info('Got Response from request_2: %s', returned)
        config['responses_recieved'].append(returned)

    LOG.info('GOT ALL RESPONSES')


config_model = {
    'required': {
        'num_req_to_send': int,
    },
    'optional': {
        'responses_recieved': str,
    }
}


connection_models = {
    'out': {
        'request_1': {
            'connection_type': 'requester',
            'required_arguments': {
                'to_echo': str,
            },
            'required_return_arguments': {
                'echoed': str,
            }
        },
        'request_2': {
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
