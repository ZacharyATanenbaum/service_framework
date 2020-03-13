""" A file to house utils that update the current state """

import logging

LOG = logging.getLogger(__name__)


def perform_delta_update(current_state, payload):
    """
    Function used to modify the current_state via a payload
    that's a whole new snapshot or a small update to the current state.
    current_state::{}
    payload = {
        'is_snapshot': bool,
        'state': {},
    }
    return::{} The new current state
    """
    LOG.debug('Performing Delta Update on Payload: %s', payload)

    for key, value in payload['state'].items():
        LOG.debug('Updating key "%s" with value "%s"', key, value)

        if value is None:
            del current_state[key]
        else:
            current_state[key] = value

    return current_state
