""" File to test service_utils """

import pytest
from service_framework.utils import service_utils, utils
from testing_utils import remove_imported_object_module


ADDRESSES_PATH = './tests/unit_tests/data/service_utils_unit_test/addresses.json'
CONFIG_PATH = './tests/unit_tests/data/service_utils_unit_test/config.json'
SERVICE_PATH = './tests/unit_tests/data/service_utils_unit_test/service.py'
WO_SERVICE_PATH = './tests/unit_tests/data/service_utils_unit_test/wo_service.py'

ENV_VARIABLES = ['env_variable_1', 'env_value_1', 'env_variable_2', 'env_value_2']


def test_service_utils__setup_addresses__no_addresses_path():
    """
    Make sure an address path does not cause any errors if not provided.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    service_utils.setup_addresses({}, imported_service, {})


def test_service_utils__setup_addresses__no_setup_addresses_func_case():
    """
    Make sure not provided setup addresses func in the imported service will not
    cause an error. (It's optional)
    """
    imported_service_wo_func = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addrs = service_utils.setup_addresses(addresses, imported_service_wo_func, {})
    assert addrs['connections']['in']['in_connection_1']['in_conn_socket_1']


def test_service_utils__setup_addresses__with_setup_addresses_func_case():
    """
    Make sure that the setup addresses func will indeed be called if provided.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    addresses = utils.get_json_from_rel_path(ADDRESSES_PATH)
    addrs = service_utils.setup_addresses(addresses, imported_service, {})
    assert addrs['connections']['in']['in_connection_1']['in_conn_socket_3']


def test_service_utils__setup_config__no_config_model_case():
    """
    Make sure to return an empty dict if there is no config model in the imported
    service. (It's optional)
    """
    wo_model_imported_service = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    config = service_utils.setup_config({}, wo_model_imported_service)
    assert config == {}


def test_service_utils__setup_config__services_setup_config_functions_properly():
    """
    Make sure that the service can call setup config prior to the config
    file being used.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    del imported_service.config_model['required']['env_variable_1']
    config = utils.get_json_from_rel_path(CONFIG_PATH)
    config = service_utils.setup_config(config, imported_service)
    assert config['optional_1'] == 'optional_value_1'
    remove_imported_object_module(imported_service)


def test_service_utils__setup_config__config_creation_is_validated():
    """
    Make sure that the setup config function actually validates what's
    provided by the config.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    del imported_service.config_model['optional']['config_2']
    config = utils.get_json_from_rel_path(CONFIG_PATH)

    with pytest.raises(ValueError):
        service_utils.setup_config(config, imported_service)


def test_service_utils__run_init_function__will_properly_call_init_function():
    """
    Test to make sure that the init_function will be called.
    """
    success = False

    def set_success_to_true(*_):
        nonlocal success
        success = True

    imported_service = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    imported_service.init_function = set_success_to_true
    service_utils.run_init_function(imported_service, {}, {}, {}, {})
    assert success


def test_service_utils__run_init_function__will_not_fail_if_init_function_not_found():
    """
    Make sure that if the init_function is not available nothing will blow up.
    """
    imported_service = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    service_utils.run_init_function(imported_service, {}, {}, {}, {})
