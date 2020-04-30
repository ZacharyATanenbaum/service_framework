""" File to house a full in  service """

from logging import getLogger
from service_framework.utils.logging_utils import get_logger

LOG = get_logger()
# Yes this should probably be a state... but I haven't created that one yet!
SENT_INTEGERS = []


def on_new_message(args, to_send, states, config):
    """
    Method triggered when a new publisher message is recieved.
    """
    LOG.info('Got new int from message: %s', args)
    SENT_INTEGERS.append(args['message_int'])


def on_new_request(args, to_send, states, config):
    """
    Method triggered when a new request is recieved from
    a requester.
    """
    global SENT_INTEGERS

    LOG.info('Got request for all sent ints')
    LOG.info('sent_integers: %s', SENT_INTEGERS)

    response = {
        'sent_message_ints': [*SENT_INTEGERS]
    }

    LOG.info('Clearing SENT_INTEGERS list after creating response.')
    SENT_INTEGERS = []

    LOG.info('Responding with: %s', response)
    return response


connection_models = {
    'in': {
        'subscribe_int': {
            'connection_type': 'subscriber',
            'optional_creation_arguments': {
                'is_binder': True
            },
            'required_creation_arguments': {
                'on_new_message': on_new_message
            },
            'required_arguments': {
                'message_int': int
            },
        },
        'reply_sent_message_ints': {
            'connection_type': 'replyer',
            'required_creation_arguments': {
                'on_new_request': on_new_request
            },
            'required_arguments': {},
            'required_return_arguments': {
                'sent_message_ints': [int],
            }
        }
    }
}
