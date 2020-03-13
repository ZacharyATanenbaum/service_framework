""" File to test service_framework.state_utils """

from decimal import Decimal
import inspect
import pytest
from service_framework.utils import state_utils

STATE_MODEL = {
    'state_type': 'full_update_out',
    'required_state_arguments': {
        'req_state_1': str,
        'req_state_2': str,
    },
    'optional_state_arguments': {
        'opt_state_1': str,
        'opt_state_2': str,
    },
    'required_arguments': {
        'req_arg_1': str,
        'req_arg_2': Decimal,
    },
    'optional_arguments': {
        'opt_arg_1': int,
        'opt_arg_2': {555: float},
    },
    'required_return_arguments': {
        'req_ret_1': str,
        'req_ret_2': [int],
    },
    'optional_return_arguments': {
        'opt_ret_1': str,
        'opt_ret_2': (int, str),
    },
}

REQUIRED_STATE = {
    'req_state_1': 'Required State Argument String 1...',
    'req_state_2': 'Required State Argument String 2...',
}

OPTIONAL_STATE = {
    'opt_state_1': 'Hi',
    'opt_state_2': '',
}

REQUIRED_ARGUMENTS = {
    'req_arg_1': 'String Hello',
    'req_arg_2': Decimal('112233.5'),
}

OPTIONAL_ARGUMENTS = {
    'opt_arg_1': 123,
    'opt_arg_2': {555: 1223.5},
}

REQUIRED_RETURN = {
    'req_ret_1': 'Hello String',
    'req_ret_2': [55]
}

OPTIONAL_RETURN = {
    'opt_ret_1': 'Optional Gello',
    'opt_ret_2': (11, 'Gello Optional'),
}


def test_state_utils__get_state_update_validator__valid_case():
    """
    Make sure when all state arguments and arguments are passed the validator
    will function correctly.
    """
    validator = state_utils.get_state_update_validator(STATE_MODEL)
    validator({
        **REQUIRED_STATE,
        **OPTIONAL_STATE,
        **REQUIRED_ARGUMENTS,
        **OPTIONAL_ARGUMENTS,
    })


def test_state_utils__get_state_update_validator__valid_req_and_opt_state_case():
    """
    Make sure both req and opt state updates function in the returned
    arg validator.
    """
    no_args_model = {**STATE_MODEL}
    del no_args_model['required_arguments']
    del no_args_model['optional_arguments']
    validator = state_utils.get_state_update_validator(no_args_model)
    validator({**REQUIRED_STATE, **OPTIONAL_STATE})


def test_state_utils__get_connection_args_validator__valid_req_conn_case():
    """
    Make sure the returned arg validator will work with no opt state arguments
    and no regular arguments.
    """
    only_required_state_update_model = {**STATE_MODEL}
    del only_required_state_update_model['required_arguments']
    del only_required_state_update_model['optional_arguments']
    del only_required_state_update_model['optional_state_arguments']
    validator = state_utils.get_state_update_validator(only_required_state_update_model)
    validator(REQUIRED_STATE)


def test_state_utils__get_state_update_validator__valid_opt_conn_case():
    """
    Make sure the returned arg validator will work with no req state arguments
    and no regular arguments.
    """
    only_optional_state_update_model = {**STATE_MODEL}
    del only_optional_state_update_model['required_arguments']
    del only_optional_state_update_model['optional_arguments']
    del only_optional_state_update_model['required_state_arguments']
    validator = state_utils.get_state_update_validator(only_optional_state_update_model)
    validator(OPTIONAL_STATE)


def test_state_utils__get_state_update_validator__valid_req_and_opt_arg_case():
    """
    Make sure both req and opt arguments in the returned arg validator.
    """
    no_state_model = {**STATE_MODEL}
    del no_state_model['required_state_arguments']
    del no_state_model['optional_state_arguments']
    validator = state_utils.get_state_update_validator(no_state_model)
    validator({**REQUIRED_ARGUMENTS, **OPTIONAL_ARGUMENTS})


def test_state_utils__get_state_update_validator__valid_req_arg_case():
    """
    Make sure the returned argument validator will work with no opt arguments
    and no state arguments.
    """
    only_required_arg_model = {**STATE_MODEL}
    del only_required_arg_model['required_state_arguments']
    del only_required_arg_model['optional_state_arguments']
    del only_required_arg_model['optional_arguments']
    validator = state_utils.get_state_update_validator(only_required_arg_model)
    validator(REQUIRED_ARGUMENTS)


def test_state_utils__get_state_update_validator__valid_opt_arg_case():
    """
    Make sure the returned argument validator will work with no req arguments
    and no state arguments.
    """
    only_optional_arg_model = {**STATE_MODEL}
    del only_optional_arg_model['required_state_arguments']
    del only_optional_arg_model['optional_state_arguments']
    del only_optional_arg_model['required_arguments']
    validator = state_utils.get_state_update_validator(only_optional_arg_model)
    validator(OPTIONAL_ARGUMENTS)


def test_state_utils__get_state_return_validator__valid_req_opt_case():
    """
    Make sure the return validator will work with both req and opt arguments.
    """
    validator = state_utils.get_state_return_validator(STATE_MODEL)
    validator({**REQUIRED_RETURN, **OPTIONAL_RETURN})


def test_state_utils__get_state_return_validator__valid_req_case():
    """
    Make sure the return validator will still work with just required args.
    """
    only_required_model = {**STATE_MODEL}
    del only_required_model['optional_return_arguments']
    validator = state_utils.get_state_return_validator(only_required_model)
    validator(REQUIRED_RETURN)


def test_state_utils__get_state_return_validator__valid_opt_case():
    """
    Make sure the return validator will work with just opt arguments.
    """
    only_optional_model = {**STATE_MODEL}
    del only_optional_model['required_return_arguments']
    validator = state_utils.get_state_return_validator(only_optional_model)
    validator(OPTIONAL_RETURN)


def test_state_utils__base_state__is_an_abstract_base_class():
    """
    Base state should be an Abstract Base Class as other connections
    should be built off of it.
    """
    base_state_class = state_utils.BaseState
    assert inspect.isabstract(base_state_class)


def test_state_utils__base_state__has_get_addresses_model_abstract_method():
    """
    Make sure the BaseState class has the abstract method of
    "get_addresses_model" that's needed for the framework.
    """
    get_addresses_model = state_utils.BaseState.get_addresses_model
    assert getattr(get_addresses_model, '__isabstractmethod__')


def test_state_utils__base_state__has_get_compatable_state_types_abstract_method():
    """
    Make sure the BaseState class has the abstract method of
    "get_compatable_state_types" that's needed for the framework.
    """
    func_to_check = state_utils.BaseState.get_compatable_state_types
    assert getattr(func_to_check, '__isabstractmethod__')


def test_state_utils__base_state__has_get_state_type_abstract_method():
    """
    Make sure the BaseState class has the abstract method of
    "get_connection_type" that's needed for the framework.
    """
    func_to_check = state_utils.BaseState.get_state_type
    assert getattr(func_to_check, '__isabstractmethod__')


def test_state_utils__base_state__has_get_creation_arguments_model_abstract_method():
    """
    Make sure the BaseState class has the abstract method of
    "get_creation_arguments_model" that's needed for the framework.
    """
    func_to_check = state_utils.BaseState.get_creation_arguments_model
    assert getattr(func_to_check, '__isabstractmethod__')


def test_state_utils__base_state__has_get_inbound_triggered_abstract_method():
    """
    Make sure the BaseState class has the abstract method of
    "get_inbound_sockets_and_triggered_functions" that's needed for the framework.
    """
    base_state_class = state_utils.BaseState
    func_to_check = base_state_class.get_inbound_sockets_and_triggered_functions
    assert getattr(func_to_check, '__isabstractmethod__')


def test_state_utils__validate_state_model__check_all_required_arguments():
    """
    Check that required arguments pass.
    """
    model = {'state_type': 'this_part_does_not_matter'}
    state_utils.validate_state_model(model)


def test_state_utils__validate_state_model__check_all_optional_arguments():
    """
    check that all optional model fields are allowed.
    """
    model = {
        'state_type':                  'this_part_still_does_not_matter',
        'required_creation_arguments': 'yawn_1',
        'optional_creation_arguments': 'yawn_2',
        'required_state_arguments':    'yawn_3',
        'optional_state_arguments':    'yawn_4',
        'required_arguments':          'yawn_5',
        'optional_arguments':          'yawn_6',
        'required_return_arguments':   'yawn_7',
        'optional_return_arguments':   'yawn_8',
    }
    state_utils.validate_state_model(model)


def test_state_utils__validate_state_model__check_error_thrown_on_illegal_arg():
    """
    Check that a field that's not in either the req or optional fields
    will cause an error.
    """
    model = {
        'state_type': 'you_get_the_idea',
        'illegal_not_optional_nor_req_field': 'yup tis bad'
    }

    with pytest.raises(ValueError):
        state_utils.validate_state_model(model)
