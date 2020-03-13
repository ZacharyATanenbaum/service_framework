""" File to conduct unit tests on the delta update in state """

import importlib

DELTA_UPDATE_IN = importlib.import_module('service_framework.states.in.delta_update_in')


def test_delta_update_in__get_addresses_model__returns_pub_and_rep_requirements():
    """
    Make sure the address model checking is set AND it doesn't change.
    """
    required_model = {
        'required_addresses': {
            'subscriber': str,
            'requester': str
        },
        'optional_addresses': {},
    }
    model = DELTA_UPDATE_IN.DeltaUpdateIn.get_addresses_model()

    assert model == required_model


def test_delta_update_in__get_compatable_state_types__returns_proper_types():
    """
    Make sure comptable state types does not decrease.
    """
    required_types = {'delta_update_out'}
    compatable_types = DELTA_UPDATE_IN.DeltaUpdateIn.get_compatable_state_types()

    for compatable in compatable_types:
        assert compatable in required_types
        required_types.remove(compatable)


def test_delta_update_in__get_creation_arguments_model__happy_case():
    """
    Make sure the proper creation arguments model is passed and no more
    required arguments are added.
    """
    required_model = {
        'required_creation_arguments': {},
        'optional_creation_arguments': {
            'topic': str,
        },
    }
    obtained_model = DELTA_UPDATE_IN.DeltaUpdateIn.get_creation_arguments_model()

    assert required_model == obtained_model


def test_delta_update_in__get_state_type__happy_case():
    """
    Make sure the state type doesn't change.
    """
    state_type = DELTA_UPDATE_IN.DeltaUpdateIn.get_state_type()

    assert state_type == 'delta_update_in'
