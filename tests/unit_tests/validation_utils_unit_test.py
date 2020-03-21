""" File to test service_framework.validation_utils """

from decimal import Decimal

import pytest

from service_framework.utils import validation_utils

REQUIRED_TEST_ARGS = {
    'test_req_dict': {'req_dict_key_1': 'req_dict_value_1'},
    'test_req_list': ['req_item_1'],
    'test_req_obj': 'req_regular_obj',
    'test_req_tuple': ('req_item_1', 123),
    'test_req_set': {'req_item_1', 'req_item_2'},
    'test_req_custom_obj': Decimal('44.44'),
    'test_req_func': lambda req_first, req_second: True,
    'test_req_set_type': {'this_is_a_set_type'},
}

OPTIONAL_TEST_ARGS = {
    'test_opt_dict': {'opt_dict_key_1': 'opt_dict_value_1'},
    'test_opt_list': ['opt_item_1'],
    'test_opt_obj': 'opt_regular_obj',
    'test_opt_tuple': ('opt_item_1', 444),
    'test_opt_set': {'opt_item_1', 'opt_item_2'},
    'test_opt_custom_obj': Decimal('55.55'),
    'test_opt_func': lambda opt_first, opt_second: True,
    'test_opt_set_type': {'this_is_an_optional_set_type'},
}

TEST_ARGS = {
    **REQUIRED_TEST_ARGS,
    **OPTIONAL_TEST_ARGS,
}

REQUIRED_ARGS_MODEL = {
    'test_req_dict': {'req_dict_key_1': str},
    'test_req_list': [str],
    'test_req_obj': str,
    'test_req_tuple': (str, int),
    'test_req_set': {'req_item_1', 'req_item_2'},
    'test_req_custom_obj': Decimal,
    'test_req_func': lambda req_first, req_second: 'Hiii',
    'test_req_set_type': {str},
}

OPTIONAL_ARGS_MODEL = {
    'test_opt_dict': {'opt_dict_key_1': str},
    'test_opt_list': [str],
    'test_opt_obj': str,
    'test_opt_tuple': (str, int),
    'test_opt_set': {'opt_item_1', 'opt_item_2'},
    'test_opt_custom_obj': Decimal,
    'test_opt_func': lambda opt_first, opt_second: 'Byyye',
    'test_opt_set_type': {str},
}


def test_validation_utils__validate_required_args__valid_all_args_provided_case():
    """
    Make sure all required args are provided.
    """
    validation_utils.validate_required_arg(REQUIRED_TEST_ARGS, REQUIRED_ARGS_MODEL)


def test_validation_utils__validate_required_args__valid_all_args_and_more_case():
    """
    Make sure the function doesn't throw an error if there are additional args
    provided.
    """
    additional_args = {
        'not_required_arg': 'Nope, not required',
        **REQUIRED_TEST_ARGS,
    }
    validation_utils.validate_required_arg(additional_args, REQUIRED_ARGS_MODEL)


def test_validation_utils__validate_required_args__invalid_not_all_args_case():
    """
    Make sure the function throws an error if not all required arguments are
    provided.
    """
    not_all_args = {**REQUIRED_TEST_ARGS}
    del not_all_args['test_req_dict']

    with pytest.raises(ValueError):
        validation_utils.validate_required_arg(not_all_args, REQUIRED_ARGS_MODEL)


def test_validation_utils__validate_optional_args__valid_some_args_provided_case():
    """
    Do not throw errors if only some optional args are provided.
    """
    not_all_args = {**OPTIONAL_TEST_ARGS}
    del not_all_args['test_opt_dict']
    validation_utils.validate_optional_arg(not_all_args, OPTIONAL_ARGS_MODEL)


def test_validation_utils__validate_optional_args__valid_all_args_provided_case():
    """
    Do not throw errors if all optional args are provided.
    """
    validation_utils.validate_optional_arg(OPTIONAL_TEST_ARGS, OPTIONAL_ARGS_MODEL)


def test_validation_utils__validate_optional_args__valid_no_args_provided_case():
    """
    Do not throw errors if no optional args are provided.
    """
    validation_utils.validate_optional_arg({}, OPTIONAL_ARGS_MODEL)


def test_validation_utils__validate_optional_args__invalid_arg_provided_case():
    """
    Do throw an error if a non-optional argument is provided.
    """
    additional_args = {
        'not_optional_arg': 'Nope, not listed in optional model',
        **OPTIONAL_TEST_ARGS,
    }

    with pytest.raises(ValueError):
        validation_utils.validate_optional_arg(additional_args, OPTIONAL_ARGS_MODEL)


def test_validation_utils__validate_args__valid_all_args_provided_case():
    """
    Don't throw an error if all args (required, optional) are provided.
    """
    validation_utils.validate_args(
        TEST_ARGS,
        REQUIRED_ARGS_MODEL,
        OPTIONAL_ARGS_MODEL
    )


def test_validation_utils__validate_args__valid_all_required_args_provided_case():
    """
    Don't throw an error if all required arguments are provided.
    """
    validation_utils.validate_args(
        REQUIRED_TEST_ARGS,
        REQUIRED_ARGS_MODEL,
        OPTIONAL_ARGS_MODEL
    )


def test_validation_utils__validate_args__invalid_not_all_required_args_case():
    """
    Throw an error if not all required args are provided.
    """
    not_all_args = {**TEST_ARGS}
    del not_all_args['test_req_dict']

    with pytest.raises(ValueError):
        validation_utils.validate_args(
            not_all_args,
            REQUIRED_ARGS_MODEL,
            OPTIONAL_ARGS_MODEL
        )


def test_validation_utils__validate_args__invalid_arg_not_specified_provided_case():
    """
    Throw an error if an invalid argument is provided.
    """
    additional_args = {
        'not_specified_arg': 'Definitely not specified',
        **TEST_ARGS,
    }

    with pytest.raises(ValueError):
        validation_utils.validate_args(
            additional_args,
            REQUIRED_ARGS_MODEL,
            OPTIONAL_ARGS_MODEL
        )


def test_validation_utils__validate_args__valid_all_args_provided_as_set_case():
    """
    Make sure that validate_args will still function if passed a set.
    """
    to_pass = {
        'req_1',
        'req_2',
        'opt_1',
        'opt_2',
    }
    required = {
        'req_1',
        'req_2',
    }
    optional = {
        'opt_1',
        'opt_2',
    }
    validation_utils.validate_args(to_pass, required, optional)
