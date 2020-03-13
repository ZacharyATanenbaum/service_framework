""" File to house a full in service """

from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def on_new_request(args, to_send, states, config):
    """
    Method triggered when a new request is recieved from
    a requester.
    """
    LOG.info('Got request for some_set_number')
    LOG.info('states: %s', states)

    response = {
        'some_set_number': states['full_in_state']['some_set_number']
    }

    LOG.info('Responding with: %s', response)
    return response


config_models = {
    'required': {
        'topic': str
    }
}


connection_models = {
    'in': {
        'reply_some_set_number': {
            'connection_type': 'replyer',
            'required_creation_arguments': {
                'on_new_request': on_new_request,
            },
            'required_arguments': {},
            'required_return_arguments': {
                'some_set_number': int,
            }
        }
    }
}


state_models = {
    'in': {
        'full_in_state': {
            'state_type': 'full_update_in',
            'optional_creation_arguments': {
                'topic': 'TEST_TOPIC',
            },
            'required_arguments': {
                'some_set_number': int,
            }
        }
    }
}
