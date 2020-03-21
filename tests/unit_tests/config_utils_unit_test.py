""" File to test: service_framework.config_utils """

import pytest
from service_framework.utils import config_utils

VALID_CONFIG_PATH = './tests/unit_tests/data/config_utils_unit_test/valid_basic_config_file.json'


def test_config_utils__get_config__valid_case():
    """
    Test that get_config works overall.
    """
    unknown_args = ['unknown_test_key_1', 'test_value_3']
    config = config_utils.get_config(VALID_CONFIG_PATH, unknown_args)

    assert config['file_test_key_1'] == 'test_value_1'
    assert config['file_test_key_2'] == 'test_value_2'
    assert config['unknown_test_key_1'] == 'test_value_3'


def test_config_utils__get_config_from_file__file_is_available_and_readable():
    """
    Read config file when file is available and readable.
    """
    config_file = config_utils.get_config_from_file(VALID_CONFIG_PATH)
    assert isinstance(config_file, dict)


def test_config_utils__get_config_from_unknown_args__valid_case():
    """
    Get config from the unknown args when passing in an even sized list.
    """
    unknown_args = [
        'key_1', 'value_1',
        'key_2', ['value', 'two'],
        '-key_3', 'value__3',
        '--key_4', 'value_4',
        'key-5', 'value_5',
        'key--6', 'value_6',
    ]
    print('Unknown Args: ', unknown_args)

    config = config_utils.get_config_from_unknown_args(unknown_args)
    print('Parsed Config: ', config)

    assert config['key_1'] == 'value_1'
    assert config['key_2'] == ['value', 'two']
    assert config['key_3'] == 'value__3'
    assert config['key_4'] == 'value_4'
    assert config['key-5'] == 'value_5'
    assert config['key--6'] == 'value_6'


def test_config_utils__get_config_from_unknown_args__unvalid_num_args_case():
    """
    Fail to get config because you cannot parse an odd list into a
    dictionary.
    """
    unknown_args = ['key_1', 'key_2', ['value', 'two']]

    with pytest.raises(ValueError):
        config_utils.get_config_from_unknown_args(unknown_args)
