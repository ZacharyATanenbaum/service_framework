""" File to house a delta out service """

import time
from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    run_test_for_full_snapshot(to_send)
    run_test_for_a_few_delta_updates(to_send)
    run_test_for_past_current_number(to_send)
    run_test_that_future_numbers_will_trigger_a_reset_state(to_send)
    LOG.info('ALL TESTING COMPLETED SUCCESSFULLY! (Well... for this file)')


def reset_downstream_state(to_send):
    """
    Needed so the following test will have a clean slate.
    """
    blank_state = {
        'current_num': -1,
        'is_snapshot': True,
        'state': {}
    }

    LOG.debug('Restting downstream state!')
    to_send('state', 'delta_state', blank_state)

    LOG.debug('Downstream state, should, be reset!')
    wait_for_state_match(blank_state['state'], to_send)

    LOG.debug('Yes, downstream state is properly reset')


def run_test_for_full_snapshot(to_send):
    """
    Test that when sending a snapshot it actually updates the downstream
    state.
    """
    reset_downstream_state(to_send)

    new_state = {'full_test_update': 'eyy_it_worked!'}

    LOG.debug('Sending Snapshot: %s', new_state)
    to_send('state', 'delta_state', {
        'current_num': 1,
        'is_snapshot': True,
        'state': new_state
    })

    LOG.debug('Checking downstream current state')
    wait_for_state_match(new_state, to_send)


def run_test_for_a_few_delta_updates(to_send):
    """
    Test that when sending delta updates it will update
    the downstream state.
    Also test that sending "None" will delete the state key.
    """
    reset_downstream_state(to_send)

    state_base = {'first_key': 'first_value'}
    first_delta = {'second_key': 'second_value'}
    second_delta = {'third_key': 'third_value'}
    third_delta = {'second_key': None}

    LOG.debug('Sending initial state: %s', state_base)
    to_send('state', 'delta_state', {
        'current_num': 1,
        'is_snapshot': True,
        'state': state_base
    })

    LOG.debug('Sending first delta: %s', first_delta)
    to_send('state', 'delta_state', {
        'current_num': 2,
        'is_snapshot': False,
        'state': first_delta
    })

    LOG.debug('Sending second delta: %s', second_delta)
    to_send('state', 'delta_state', {
        'current_num': 3,
        'is_snapshot': False,
        'state': second_delta
    })

    LOG.debug('Sending third delta: %s', third_delta)
    to_send('state', 'delta_state', {
        'current_num': 4,
        'is_snapshot': False,
        'state': third_delta
    })

    expected_state = {**state_base, **second_delta}
    wait_for_state_match(expected_state, to_send)
    LOG.debug('Getting downstream state...')


def run_test_for_past_current_number(to_send):
    """
    Test that messages sent before the current snapshot
    are disregarded.
    """
    reset_downstream_state(to_send)

    state_base = {'first_key': 'first_value'}
    first_delta = {'second_key': 'second_value'}
    second_delta = {'third_key': 'third_value'}

    LOG.debug('Sending initial state: %s', state_base)
    to_send('state', 'delta_state', {
        'current_num': 1,
        'is_snapshot': True,
        'state': state_base
    })

    LOG.debug('Sending first delta: %s', first_delta)
    to_send('state', 'delta_state', {
        'current_num': -100,
        'is_snapshot': False,
        'state': first_delta
    })

    LOG.debug('Sending second delta: %s', second_delta)
    to_send('state', 'delta_state', {
        'current_num': 2,
        'is_snapshot': False,
        'state': second_delta
    })

    # Need a new object as sending the incorrect current_num will
    # mess up the state between the output and input delta states.
    expected = {
        'first_key': 'first_value',
        'third_key': 'third_value',
    }
    LOG.debug('Getting downstream state...')
    wait_for_state_match(expected, to_send)


def run_test_that_future_numbers_will_trigger_a_reset_state(to_send):
    """
    Make sure if the downstream service gets a current number that's larger
    than the next expected number to request the current state from the
    sender.
    """
    reset_downstream_state(to_send)

    state_base = {'first_key': 'first_value'}
    first_delta = {'second_key': 'second_value'}
    second_delta = {'third_key': 'third_value'}
    third_delta = {'second_key': None}

    LOG.debug('Sending initial state: %s', state_base)
    to_send('state', 'delta_state', {
        'current_num': 0,
        'is_snapshot': True,
        'state': state_base
    })

    LOG.debug('Sending first delta: %s', first_delta)
    to_send('state', 'delta_state', {
        'current_num': 1,
        'is_snapshot': False,
        'state': first_delta
    })

    LOG.debug('Sending second delta: %s', second_delta)
    to_send('state', 'delta_state', {
        'current_num': 100,
        'is_snapshot': False,
        'state': second_delta
    })

    LOG.debug('Sending third delta: %s', third_delta)
    to_send('state', 'delta_state', {
        'current_num': 101,
        'is_snapshot': False,
        'state': third_delta
    })

    expected_state = {**state_base, **second_delta}
    LOG.debug('Getting downstream state...')
    wait_for_state_match(expected_state, to_send)


def wait_for_state_match(desired, to_send, time_to_wait_s=0.5):
    """
    This function is used to check if the state of the connected delta_update_in
    service's downstream state has updated and if it matches the desired output.
    desired::{} The desired output state
    to_send::def(str, str, dict) The to_send function provided to main
    time_to_wait::int The time to wait prior to assuming the response is not correct
    """
    response = None
    start_time = time.time()

    while response != desired and time.time() - start_time < time_to_wait_s:
        response = to_send('connection', 'current_downstream_state', {})
        time.sleep(0.01)

    LOG.debug('Downstream State %s - Desired %s', response['current_state'], desired)
    assert response is not None
    assert response['current_state'] == desired


connection_models = {
    'out': {
        'current_downstream_state': {
            'connection_type': 'requester',
            'required_return_arguments': {
                'current_state': dict,
            }
        }
    }
}


state_models = {
    'out': {
        'delta_state': {
            'state_type': 'delta_update_out',
            'required_state_arguments': {
                'current_num': int,
                'is_snapshot': bool
            },
            'required_arguments': {
                'state': dict
            },
        }
    }
}
