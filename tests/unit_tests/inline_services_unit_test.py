""" File that houses all of the integration tests for the Service class """

import pytest

from service_framework import InlineServices
from service_framework.utils.utils import import_python_file_from_cwd


def test_inline_services__services_can_be_run_with_paths():
    """
    Make sure that services can be run together with inline services
    provided via paths.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH)
    inline.add_relation('requester', 'request', 'replyer', 'reply')
    inline.start()

    req_config = inline.get_service_config('requester')
    assert len(req_config['responses_recieved']) == 2

def test_inline_services__services_by_path_can_have_provided_config():
    """
    Make sure that services, when run by path, can have a pre-existing
    config provided.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH, REPLYER_CONFIG)
    inline.add_relation('requester', 'request', 'replyer', 'reply')
    inline.start()

    req_config = inline.get_service_config('requester')
    assert len(req_config['responses_recieved']) == 2
    assert REPLYER_CONFIG['response_text'] in req_config['responses_recieved'][0]['echoed']


def test_inline_services__main_by_path_can_have_provided_config():
    """
    Make sure that services, when run by path, can have a pre-existing
    config provided.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH, REQUESTER_CONFIG)
    inline.add_service('replyer', REPLYER_PATH)
    inline.add_relation('requester', 'request', 'replyer', 'reply')
    inline.start()

    req_config = inline.get_service_config('requester')
    assert len(req_config['responses_recieved']) == 4


def test_inline_services__services_can_be_run_with_imported_modules():
    """
    Make sure that services can be run together with inline services
    provided via modules.
    """
    inline = InlineServices()
    inline.set_main_service_by_module(
        'requester',
        import_python_file_from_cwd(REQUESTER_PATH)
    )
    inline.add_service_by_module(
        'replyer',
        import_python_file_from_cwd(REPLYER_PATH)
    )
    inline.add_relation('requester', 'request', 'replyer', 'reply')
    inline.start()

    req_config = inline.get_service_config('requester')
    assert len(req_config['responses_recieved']) == 2


def test_inline_services__services_by_module_can_have_provided_config():
    """
    Make sure that an added service, by module, can have a provided
    config.
    """
    inline = InlineServices()
    inline.set_main_service_by_module(
        'requester',
        import_python_file_from_cwd(REQUESTER_PATH)
    )
    inline.add_service_by_module(
        'replyer',
        import_python_file_from_cwd(REPLYER_PATH),
        REPLYER_CONFIG
    )
    inline.add_relation('requester', 'request', 'replyer', 'reply')
    inline.start()

    req_config = inline.get_service_config('requester')
    assert len(req_config['responses_recieved']) == 2
    assert REPLYER_CONFIG['response_text'] in req_config['responses_recieved'][0]['echoed']


def test_inline_services__main_by_module_can_have_provided_config():
    """
    Make sure that a main service, by module, can have a provided
    config.
    """
    inline = InlineServices()
    inline.set_main_service_by_module(
        'requester',
        import_python_file_from_cwd(REQUESTER_PATH),
        REQUESTER_CONFIG
    )
    inline.add_service_by_module(
        'replyer',
        import_python_file_from_cwd(REPLYER_PATH),
    )
    inline.add_relation('requester', 'request', 'replyer', 'reply')
    inline.start()

    req_config = inline.get_service_config('requester')
    assert len(req_config['responses_recieved']) == 4

def test_inline_services__set_main_service_not_providing_a_string_path_throws_error():
    """
    Make sure that if setting a main service and accidentally passing a
    module a ValueError will be thrown.
    """
    inline = InlineServices()
    with pytest.raises(ValueError):
        inline.set_main_service(
            'requester',
            import_python_file_from_cwd(REQUESTER_PATH)
        )

def test_inline_services__add_service_not_providing_a_string_path_throws_error():
    """
    Make sure that if adding a service and accidentally passing a module
    a ValueError will be thrown.
    """
    inline = InlineServices()
    with pytest.raises(ValueError):
        inline.add_service(
            'replyer',
            import_python_file_from_cwd(REPLYER_PATH),
        )

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


def test_setup_service__validate_setup_service_calls_setup_conifg():
    """
    """


def test_get_to_send__to_send_functions_properly():
    """
    """


def test_get_to_send__to_send_functions_with_return():
    """
    """


def test_get_to_send__to_send_functions_with_publisher():
    """
    """


def test_get_to_send__to_send_functions_with_requester():
    """
    """


def test_get_to_send__to_send_will_only_allow_one_return():
    """
    """


def test_get_service_module__happy_case():
    """
    """


def test_get_service_module__service_name_dne_and_throws_error_case():
    """
    """


def test_get_service_config__happy_case():
    """
    """


def test_get_service_config__service_name_dne_and_throws_error_case():
    """
    """


BASE_DIR = './tests/unit_tests/data/inline_service_integration_test'

DO_NOTHING_PATH = f'{BASE_DIR}/do_nothing_service.py'
REPLYER_PATH = f'{BASE_DIR}/replyer_service.py'
REQUESTER_PATH = f'{BASE_DIR}/requester_service.py'

REQUESTER_CONFIG = {
    'num_req_to_send': 4
}

REPLYER_CONFIG = {
    'response_text': 'NEW_TEXT!'
}
