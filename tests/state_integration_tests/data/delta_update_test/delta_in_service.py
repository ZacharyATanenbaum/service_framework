""" File to house a delta in service """

from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def on_new_request(args, to_send, states, config):
    """
    Method triggered when a new request is recieved from
    a requester.
    """
    LOG.debug('Got request for the current state')
    LOG.debug('states: %s', states)

    response = {'current_state': states['delta_state']}

    LOG.debug('Responding with: %s', response)
    return response


connection_models = {
    'in': {
        'current_downstream_state': {
            'connection_type': 'replyer',
            'required_creation_arguments': {
                'on_new_request': on_new_request,
            },
            'required_return_arguments': {
                'current_state': dict,
            }
        }
    }
}


state_models = {
    'in': {
        'delta_state': {
            'state_type': 'delta_update_in',
            'required_state_arguments': {
                'current_num': int,
                'is_snapshot': bool
            },
            'required_arguments': {
                'state': dict
            }
        }
    }
}
