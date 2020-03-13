""" File to house a full out service """

import time
from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    nums_to_send = [111, 222]

    for num in nums_to_send:
        LOG.info('Sending some_set_number: %s', num)

        to_send(
            'state',
            'full_out_state',
            {'some_set_number': num}
        )

        LOG.info('Checking if state was updated...')
        response = to_send('connection', 'get_some_set_number', {})
        got_some_set_number = response['some_set_number']

        LOG.info('Got "%s" should be "%s"', got_some_set_number, num)
        assert got_some_set_number == num


connection_models = {
    'out': {
        'get_some_set_number': {
            'connection_type': 'requester',
            'required_arguments': {},
            'required_return_arguments': {
                'some_set_number': int,
            }
        }
    }
}


state_models = {
    'out': {
        'full_out_state': {
            'state_type': 'full_update_out',
            'optional_creation_arguments': {
                'topic': 'TEST_TOPIC',
                'is_x_pub': True
            },
            'required_arguments': {
                'some_set_number': int,
            },
        }
    }
}
