""" File to house a full out service """

import time
from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    nums_to_send = list(range(10))

    for num in nums_to_send:
        LOG.info('Publishing int: %s', num)

        to_send(
            'connection',
            'publish_int',
            {'message_int': num}
        )

    # Wait for all publisher messages to be collected
    time.sleep(0.2)

    LOG.info('Checking if messages where recieved...')
    response = to_send('connection', 'get_sent_message_ints', {})
    sent_message_ints = response['sent_message_ints']

    LOG.info('Got "%s" should be "%s"', sent_message_ints, nums_to_send)
    assert sent_message_ints == nums_to_send


connection_models = {
    'out': {
        'publish_int': {
            'connection_type': 'publisher',
            'optional_creation_arguments': {
                'is_x_pub': True
            },
            'required_arguments': {
                'message_int': int
            }
        },
        'get_sent_message_ints': {
            'connection_type': 'requester',
            'required_arguments': {},
            'required_return_arguments': {
                'sent_message_ints': [int],
            }
        }
    }
}
