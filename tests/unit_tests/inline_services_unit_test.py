""" File that houses all of the integration tests for the Service class """

from service_framework import InlineServices
from service_framework.utils.utils import import_python_file_from_cwd


def test_inline_services__services_can_be_run_with_paths():
    """
    Make sure that services can be run together with inline services
    provided via paths.
    """
    # TODO: Finish this file
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH, REQUESTER_CONFIG)
    inline.add_relation('requester', 'request', 'replyer', 'reply')
    inline.start()



def test_inline_services__services_can_be_run_with_imported_modules():
    """
    Make sure that services can be run together with inline services
    provided via paths.
    """


def test_inline_services__can_have_multiple_dependent_services():
    """
    Make sure that one main service can call multiple dependent services.
    """


def test_inline_services__service_calls_multiple_relations():
    """
    """


def test_add_service__adding_service_with_same_name_errors():
    """
    """


def test_add_service_as_module__adding_service_with_same_name_errors():
    """
    """


def test_set_main_service__setting_service_with_same_name_errors():
    """
    """


def test_set_main_service_as_module__setting_service_with_same_name_errors():
    """
    """


def test_set_main_service__adding_second_main_service_throws_error():
    """
    """


def test_set_main_service_as_module__adding_second_main_service_throws_error():
    """
    """


def test_start__starting_without_main_service_throws_error():
    """
    """


def test_inline_services__adding_relation_with_improper_out_service_name_throws_error():
    """
    """


def test_inline_services__adding_relation_with_improper_in_service_name_throws_error():
    """
    """


def test_setup_service__validate_setup_service_sets_up_sigint_handler():
    """
    """


def test_setup_service__validate_setup_service_sets_up_sigterm_handler():
    """
    """


BASE_DIR = './tests/unit_tests/data/inline_service_integration_test'

DO_NOTHING_PATH = f'{BASE_DIR}/do_nothing_service.py'
REPLYER_PATH = f'{BASE_DIR}/replyer_service.py'
REQUESTER_PATH = f'{BASE_DIR}/requester_service.py'

REQUESTER_CONFIG = {
    'num_req_to_send': 2
}
