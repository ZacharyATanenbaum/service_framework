""" Integration Test File for service_framework.connection_utils.py """

import logging
import pytest
from service_framework.utils import state_utils
from service_framework.states.out.full_update_out import FullUpdateOut

LOG = logging.getLogger(__name__)


ADDRESSES = {
    'states': {
        'out': {
            'full_update_1': {
                'publisher': '127.0.0.1:8877',
            },
            'full_update_2': {
                'publisher': '127.0.0.1:8888',
            },
        }
    }
}


STATE_MODELS = {
    'out': {
        'full_update_1': {
            'state_type': 'full_update_out',
            'optional_creation_arguments': {
                'wait_after_creation_s': 0.0
            }
        },
        'full_update_2': {
            'state_type': 'full_update_out',
            'optional_creation_arguments': {
                'wait_after_creation_s': 0.0
            },
        },
    },
}


BASIC_ADDRESSES = {
    'required_addr_1': 'req_string_address_1',
    'required_addr_2': 'req_string_address_2',
    'optional_addr_1': 'opt_string_address_1',
    'optional_addr_2': 'opt_string_address_2',
}


BASIC_MODEL = {
    'state_type': 'basic',
    'required_creation_arguments': {
        'required_creation_argument_1': 'foo',
        'required_creation_argument_2': 7888,
    },
    'optional_creation_arguments': {
        'optional_creation_argument_1': 'bar',
        'optional_creation_argument_2': 1337,
    },
}


def test_state_utils__base_state__valid_validate_creation_args_and_addresses_case():
    """
    Make sure the addresses provided to a state are validated in the base
    state.
    """
    BaseTestingState(BASIC_MODEL, BASIC_ADDRESSES)


def test_state_utils__base_state__invalid_validate_addresses_case():
    """
    Make sure the addresses provided to a state are validated in the base
    state.
    """
    not_all_required_addresses = {**BASIC_ADDRESSES}
    del not_all_required_addresses['required_addr_1']

    with pytest.raises(ValueError):
        BaseTestingState({}, not_all_required_addresses)


def test_state_utils__base_state__invalid_validate_creation_args_case():
    """
    Make sure the creation arguments provided to a state are validated in
    the base state.
    """
    no_required_args = {**BASIC_MODEL}
    del no_required_args['required_creation_arguments']

    with pytest.raises(ValueError):
        BaseTestingState(no_required_args, {})


def test_state_utils__base_state__normal_send_function_throws_error():
    """
    Make sure that calling the "send" function without overwriting
    it will throw a Runtime error.
    """
    state = BaseTestingState(BASIC_MODEL, BASIC_ADDRESSES)

    with pytest.raises(RuntimeError):
        state.send({})


def test_state_utils__get_state__valid_get_full_update_out_case():
    """
    Test if the get_connection function can make a full_update_out state.
    """
    address = ADDRESSES['states']['out']['full_update_1']
    model = STATE_MODELS['out']['full_update_1']

    state = state_utils.get_state(
        model,
        'out',
        address
    )

    assert isinstance(state, FullUpdateOut)


def test_state_utils__setup_states__valid_get_full_update_outs_case():
    """
    Test if setup_state will get all of the full update outs provided.
    """
    states = state_utils.setup_states(STATE_MODELS, ADDRESSES)
    state_1 = states['out']['full_update_1']
    state_2 = states['out']['full_update_2']

    assert isinstance(state_1, FullUpdateOut)
    assert isinstance(state_2, FullUpdateOut)


class BaseTestingState(state_utils.BaseState):
    """
    Framework for creating a new State
    """
    @staticmethod
    def get_addresses_model():
        """
        This is needed so the BaseState can validate the
        provided addresses and throw an error if any are missing.
        As well as automatically generate documentation.
        NOTE: types must always be "str"
        return = {
            'required_addresses': {
                'req_address_name_1': str,
                'req_address_name_2': str,
            },
            'optional_addresses': {
                'opt_address_name_1': str,
                'opt_address_name_2': str,
            },
        }
        """
        return {
            'required_addresses': {
                'required_addr_1': str,
                'required_addr_2': str,
            },
            'optional_addresses': {
                'optional_addr_1': str,
                'optional_addr_2': str,
            },
        }

    @staticmethod
    def get_compatable_state_types():
        """
        This is needed so the service framework knows which
        states this current state is compatable.
        return::['str'] A list of the compatable state, update types.
        """
        return ['basic']

    @staticmethod
    def get_creation_arguments_model():
        """
        This is needed so the BaseState can validate the provided
        creation arguments as well as for auto documentation.
        return = {
            'required_creation_arguments': {
                'required_creation_arg_1': type,
                'required_creation_arg_2': type,
            },
            'optional_creation_arguments': {
                'optional_creation_arg_1': type,
                'optional_creation_arg_2': type,
            },
        }
        """
        return {
            'required_creation_arguments': {
                'required_creation_argument_1': str,
                'required_creation_argument_2': int,
            },
            'optional_creation_arguments': {
                'optional_creation_argument_1': str,
                'optional_creation_argument_2': int,
            },
        }

    @staticmethod
    def get_state_arguments_model():
        """
        This is needed so the BaseState can validate the provided
        model has the required or optional arguments for the state
        to function.
        return = {
            'required_state_arguments': {
                'required_state_arg_1': type,
                'required_state_arg_2': type,
            },
            'optional_state_arguments': {
                'optional_state_arg_1': type,
                'optional_state_arg_2': type,
            },
        }
        """
        return {
            'required_state_arguments': {},
            'required_State_arguments': {},
        }

    @staticmethod
    def get_state_type():
        """
        This is needed so the service framework knows the
        state type of the current state.
        return::str The state and update type of this state.
        """
        return 'basic'

    def get_inbound_sockets_and_triggered_functions(self):
        """
        Method needed so the service framework knows which sockets to listen
        for new messages and what functions to call when a message appears.
        return [{
            'inbound_socket': zmq.Context.Socket,
            'arg_validator': def(args),
            'connection_function': def(args, log) -> args or None,
            'model_function': def(args, to_send, states, conifg, log) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args, log),
        }]
        """
        return []

    def runtime_setup(self):
        """
        This method is used for the state to do any setup that must occur during
        runtime. I.E. setting up a zmq.Context.
        """
