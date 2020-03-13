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
    Make sure an address path must be provided.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)

    with pytest.raises(ValueError):
        service_utils.setup_addresses(None, imported_service, {})


def test_service_utils__setup_addresses__no_setup_addresses_func_case():
    """
    Make sure not provided setup addresses func in the imported service will not
    cause an error. (It's optional)
    """
    imported_service_wo_func = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    addrs = service_utils.setup_addresses(ADDRESSES_PATH, imported_service_wo_func, {})
    assert addrs['connections']['in']['in_connection_1']['in_conn_socket_1']


def test_service_utils__setup_addresses__with_setup_addresses_func_case():
    """
    Make sure that the setup addresses func will indeed be called if provided.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    addrs = service_utils.setup_addresses(ADDRESSES_PATH, imported_service, {})
    assert addrs['connections']['in']['in_connection_1']['in_conn_socket_3']


def test_service_utils__setup_config__no_config_model_case():
    """
    Make sure to return an empty dict if there is no config model in the imported
    service. (It's optional)
    """
    wo_model_imported_service = utils.import_python_file_from_cwd(WO_SERVICE_PATH)
    config = service_utils.setup_config(CONFIG_PATH, {}, wo_model_imported_service)
    assert config == {}


def test_service_utils__setup_config__imports_config_from_file():
    """
    Make sure if the config model is provided, config information is taken
    from the config path.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    imported_service.config_model = {**imported_service.config_model}
    del imported_service.config_model['required']['env_variable_1']
    del imported_service.setup_config
    config = service_utils.setup_config(CONFIG_PATH, {}, imported_service)
    assert config['config_1'] == 'value_1'
    remove_imported_object_module(imported_service)


def test_service_utils__setup_config__services_setup_config_functions_properly():
    """
    Make sure that the service can call setup config prior to the config
    file being used.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    del imported_service.config_model['required']['env_variable_1']
    config = service_utils.setup_config(CONFIG_PATH, {}, imported_service)
    assert config['optional_1'] == 'optional_value_1'
    remove_imported_object_module(imported_service)


def test_service_utils__setup_config__config_creation_is_validated():
    """
    Make sure that the setup config function actually validates what's
    provided by the config.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    del imported_service.config_model['optional']['config_2']

    with pytest.raises(ValueError):
        service_utils.setup_config(CONFIG_PATH, {}, imported_service)


def test_service_utils__setup_config__imports_config_from_unknown_env_args():
    """
    Make sure that environmental arguments that aren't know are added to the
    config dict.
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    del imported_service.config_model['required']['config_1']
    config = service_utils.setup_config('', ENV_VARIABLES, imported_service)
    assert config['env_variable_1'] == 'env_value_1'
    remove_imported_object_module(imported_service)


def test_service_utils__setup_config__imports_config_from_env_args_and_file():
    """
    Make sure that both config args and the config file will actually provide
    variables to the config...
    """
    imported_service = utils.import_python_file_from_cwd(SERVICE_PATH)
    service_utils.setup_config(CONFIG_PATH, ENV_VARIABLES, imported_service)
    remove_imported_object_module(imported_service)
