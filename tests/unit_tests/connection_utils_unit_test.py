""" File to test service_framework.connection_utils """

from decimal import Decimal
import inspect
import pytest
from service_framework.utils import connection_utils

CONNECTION_MODEL = {
    'connection_type': 'replyer',
    'required_connection_arguments': {
        'req_con_1': str,
        'req_con_2': str,
    },
    'optional_connection_arguments': {
        'opt_con_1': str,
        'opt_con_2': str,
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

REQUIRED_CONNECTION = {
    'req_con_1': 'Required Connection Argument String 1...',
    'req_con_2': 'Required Connection Argument String 2...',
}

OPTIONAL_CONNECTION = {
    'opt_con_1': 'Hi',
    'opt_con_2': '',
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


def test_connection_utils__get_connection_args_validator__valid_case():
    """
    Make sure when all connection arguments and arguments are passed the validator
    will function correctly.
    """
    validator = connection_utils.get_connection_args_validator(CONNECTION_MODEL)
    validator({
        **REQUIRED_CONNECTION,
        **OPTIONAL_CONNECTION,
        **REQUIRED_ARGUMENTS,
        **OPTIONAL_ARGUMENTS,
    })


def test_connection_utils__get_connection_args_validator__valid_req_and_opt_conn_case():
    """
    Make sure both req and opt connection arguments function in the returned
    arg validator.
    """
    no_args_model = {**CONNECTION_MODEL}
    del no_args_model['required_arguments']
    del no_args_model['optional_arguments']
    validator = connection_utils.get_connection_args_validator(no_args_model)
    validator({**REQUIRED_CONNECTION, **OPTIONAL_CONNECTION})


def test_connection_utils__get_connection_args_validator__valid_req_conn_case():
    """
    Make sure the returned arg validator will work with no opt connection arguments
    and no regular arguments.
    """
    only_required_conn_arg_model = {**CONNECTION_MODEL}
    del only_required_conn_arg_model['required_arguments']
    del only_required_conn_arg_model['optional_arguments']
    del only_required_conn_arg_model['optional_connection_arguments']

    print(only_required_conn_arg_model)

    validator = connection_utils.get_connection_args_validator(only_required_conn_arg_model)
    validator(REQUIRED_CONNECTION)


def test_connection_utils__get_connection_args_validator__valid_opt_conn_case():
    """
    Make sure the returned arg validator will work with no req connection arguments
    and no regular arguments.
    """
    only_optional_conn_arg_model = {**CONNECTION_MODEL}
    del only_optional_conn_arg_model['required_arguments']
    del only_optional_conn_arg_model['optional_arguments']
    del only_optional_conn_arg_model['required_connection_arguments']
    validator = connection_utils.get_connection_args_validator(only_optional_conn_arg_model)
    validator(OPTIONAL_CONNECTION)


def test_connection_utils__get_connection_args_validator__valid_req_and_opt_arg_case():
    """
    Make sure both req and opt arguments in the returned arg validator.
    """
    no_conn_model = {**CONNECTION_MODEL}
    del no_conn_model['required_connection_arguments']
    del no_conn_model['optional_connection_arguments']
    validator = connection_utils.get_connection_args_validator(no_conn_model)
    validator({**REQUIRED_ARGUMENTS, **OPTIONAL_ARGUMENTS})


def test_connection_utils__get_connection_args_validator__valid_req_arg_case():
    """
    Make sure the returned argument validator will work with no opt arguments
    and no connection arguments.
    """
    only_required_arg_model = {**CONNECTION_MODEL}
    del only_required_arg_model['required_connection_arguments']
    del only_required_arg_model['optional_connection_arguments']
    del only_required_arg_model['optional_arguments']
    validator = connection_utils.get_connection_args_validator(only_required_arg_model)
    validator(REQUIRED_ARGUMENTS)


def test_connection_utils__get_connection_args_validator__valid_opt_arg_case():
    """
    Make sure the returned argument validator will work with no req arguments
    and no connection arguments.
    """
    only_optional_arg_model = {**CONNECTION_MODEL}
    del only_optional_arg_model['required_connection_arguments']
    del only_optional_arg_model['optional_connection_arguments']
    del only_optional_arg_model['required_arguments']
    validator = connection_utils.get_connection_args_validator(only_optional_arg_model)
    validator(OPTIONAL_ARGUMENTS)


def test_connection_utils__get_connection_return_validator__valid_req_opt_case():
    """
    Make sure the return validator will work with both req and opt arguments.
    """
    validator = connection_utils.get_connection_return_validator(CONNECTION_MODEL)
    validator({**REQUIRED_RETURN, **OPTIONAL_RETURN})


def test_connection_utils__get_connection_return_validator__valid_req_case():
    """
    Make sure the return validator will still work with just required args.
    """
    only_required_model = {**CONNECTION_MODEL}
    del only_required_model['optional_return_arguments']
    validator = connection_utils.get_connection_return_validator(only_required_model)
    validator(REQUIRED_RETURN)


def test_connection_utils__get_connection_return_validator__valid_opt_case():
    """
    Make sure the return validator will work with just opt arguments.
    """
    only_optional_model = {**CONNECTION_MODEL}
    del only_optional_model['required_return_arguments']
    validator = connection_utils.get_connection_return_validator(only_optional_model)
    validator(OPTIONAL_RETURN)


def test_connection_utils__base_connection__is_an_abstract_base_class():
    """
    Base connection should be an Abstract Base Class as other connections
    should be built off of it.
    """
    base_connection_class = connection_utils.BaseConnection
    assert inspect.isabstract(base_connection_class)


def test_connection_utils__base_connection__has_get_addresses_model_abstract_method():
    """
    Make sure the BaseConnection class has the abstract method of
    "get_addresses_model" that's needed for the framework.
    """
    get_addresses_model = connection_utils.BaseConnection.get_addresses_model
    assert getattr(get_addresses_model, '__isabstractmethod__')


def test_connection_utils__base_connection__has_get_creation_arguments_model_abstract_method():
    """
    Make sure the BaseConnection class has the abstract method of
    "get_creation_arguments_model" that's needed for the framework.
    """
    func_to_check = connection_utils.BaseConnection.get_creation_arguments_model
    assert getattr(func_to_check, '__isabstractmethod__')


def test_connection_utils__base_connection__has_get_inbound_triggered_abstract_method():
    """
    Make sure the BaseConnection class has the abstract method of
    "get_inbound_sockets_and_triggered_functions" that's needed for the framework.
    """
    base_connection_class = connection_utils.BaseConnection
    func_to_check = base_connection_class.get_inbound_sockets_and_triggered_functions
    assert getattr(func_to_check, '__isabstractmethod__')


def test_connection_utils__validate_connection_model__check_all_required_args():
    """
    Check that required arguments pass.
    """
    model = {'connection_type': 'this_part_does_not_matter'}
    connection_utils.validate_connection_model(model)


def test_connection_utils__validate_connection_model__check_all_optional_args():
    """
    check that all optional model fields are allowed.
    """
    model = {
        'connection_type':               'this_part_still_does_not_matter',
        'required_creation_arguments':   'yawn_1',
        'optional_creation_arguments':   'yawn_2',
        'required_connection_arguments': 'yawn_3',
        'optional_connection_arguments': 'yawn_4',
        'required_arguments':            'yawn_5',
        'optional_arguments':            'yawn_6',
        'required_return_arguments':     'yawn_7',
        'optional_return_arguments':     'yawn_8',
    }
    connection_utils.validate_connection_model(model)


def test_connection_utils__validate_connection_model__error_thrown_on_illegal_arg():
    """
    Check that a field that's not in either the req or optional fields
    will cause an error.
    """
    model = {
        'connection_type': 'you_get_the_idea',
        'illegal_not_optional_nor_req_field': 'yup tis bad'
    }

    with pytest.raises(ValueError):
        connection_utils.validate_connection_model(model)
