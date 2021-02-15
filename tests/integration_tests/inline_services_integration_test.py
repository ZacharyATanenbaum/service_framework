""" File that houses all of the integration tests for the Service class """

from service_framework import InlineServices
from service_framework.utils.utils import import_python_file_from_cwd


def test_inline_services__services_can_be_run_with_paths():
    """
    Make sure that services can be run together with inline services
    provided via paths.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH, {

    })


def test_inline_services__services_can_be_run_with_imported_modules():
    """
    Make sure that services can be run together with inline services
    provided via paths.
    """


def test_inline_services__can_have_multiple_dependent_services():
    """
    Make sure that one main service can call multiple dependent services.
    """



BASE_DIR = './tests/integration_tests'
BASE_LOG_DIR = f'{BASE_DIR}/logs/service_integration_test/service_can_be_run_programmatically'

DO_NOTHING_PATH = f'{BASE_DIR}/data/service_integration_test/do_nothing_service.py'
REPLYER_PATH = f'{BASE_DIR}/data/service_integration_test/replyer_service.py'
REQUESTER_PATH = f'{BASE_DIR}/data/service_integration_test/requester_service.py'

REQUESTER_CONFIG = {
    'num_req_to_send': 2
}
