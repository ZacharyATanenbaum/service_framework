""" Basic service for testing the service_utils """

from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def setup_connection_models(models, config):
    """
    This function is used to modify the needed connections prior to initializing
    said connections.
    models::{}
    return::{}
    """
    models['out'] = {
        'out_connection_1': {
            'connection_type': 'requester',
            'required_arguments': {
                'this_is_a_test_arg': str,
            },
            'required_return_arguments': {
                'this_is_a_return_arg': str,
            },
        }
    }
    return models


def on_new_request(args, to_send, config):
    """
    This function is needed to respond to a request message from a requester.
    """
    LOG.info('%s, %s, %s, %s', args, to_send, states, config)
    return {}


connection_models = {
    'in': {
        'in_connection_1': {
            'connection_type': 'replyer',
            'required_creation_arguments': {
                'on_new_request': on_new_request,
            },
            'required_arguments': {
                'this_is_a_test_arg': str,
            },
            'required_return_arguments': {
                'this_is_a_return_arg': str,
            },
        },
    },
}
