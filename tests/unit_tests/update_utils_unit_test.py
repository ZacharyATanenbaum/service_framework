""" File to unit test the service_framework update_utils file """

from service_framework.utils import update_utils


CURRENT_STATE = {
    'current_key': 'current_val',
}

BASE_PAYLOAD = {
    'is_snapshot': bool,
    'state': {}
}


def test_update_utils__perform_delta_update__is_delta_add_to_state_case():
    """
    Make sure a delta update will add a new key to the current state.
    """
    add_payload = {**BASE_PAYLOAD}
    add_payload['is_snapshot'] = False

    to_add = {'new_key': 'new_val'}
    add_payload['state'] = to_add
    should_be_new_state = {**CURRENT_STATE, **to_add}

    new_state = update_utils.perform_delta_update(CURRENT_STATE, add_payload)
    assert new_state == should_be_new_state


def test_update_utils__perform_delta_update__is_delta_remove_from_state_case():
    """
    Make sure a delta update will remove a key from the current state.
    """
    remove_payload = {**BASE_PAYLOAD}
    remove_payload['is_snapshot'] = False

    to_remove = {'current_key': None}
    remove_payload['state'] = to_remove

    should_be_new_state = {**CURRENT_STATE}
    for key in to_remove:
        del should_be_new_state[key]

    new_state = update_utils.perform_delta_update(CURRENT_STATE, remove_payload)
    assert new_state == should_be_new_state


def test_update_utils__perform_delta_update__is_delta_update_state_case():
    """
    Make sure a delta update will update a key in the current state.
    """
    update_payload = {**BASE_PAYLOAD}
    update_payload['is_snapshot'] = False

    to_update = {'current_key': 'new_value'}
    update_payload['state'] = to_update

    should_be_new_state = {**CURRENT_STATE}
    for key, value in to_update.items():
        should_be_new_state[key] = value

    new_state = update_utils.perform_delta_update(CURRENT_STATE, update_payload)
    assert new_state == should_be_new_state
