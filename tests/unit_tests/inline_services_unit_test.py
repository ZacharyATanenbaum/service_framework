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


def test_inline_services__service_calls_multiple_relations():
    """
    Make sure that one main service can call multiple dependent services.
    """
    inline = InlineServices()
    inline.set_main_service('multi_requester', MULTI_REQUESTER_PATH)
    inline.add_service('replyer_1', REPLYER_PATH)
    inline.add_relation('multi_requester', 'request_1', 'replyer_1', 'reply')
    inline.add_service('replyer_2', REPLYER_PATH)
    inline.add_relation('multi_requester', 'request_2', 'replyer_2', 'reply')
    inline.start()

    req_config = inline.get_service_config('multi_requester')
    assert len(req_config['responses_recieved']) == 4


def test_add_service__adding_service_with_same_name_errors():
    """
    Adding a server with the same name as another service should error.
    """
    inline = InlineServices()
    inline.add_service('replyer', REPLYER_PATH)

    with pytest.raises(ValueError):
        inline.add_service('replyer', REPLYER_PATH)


def test_add_service_as_module__adding_service_with_same_name_errors():
    """
    Adding a server, as module, with the same name as another service
    should error.
    """
    inline = InlineServices()
    inline.add_service_by_module(
        'replyer',
        import_python_file_from_cwd(REPLYER_PATH)
    )

    with pytest.raises(ValueError):
        inline.add_service_by_module(
            'replyer',
            import_python_file_from_cwd(REPLYER_PATH)
        )


def test_set_main_service__setting_service_with_same_name_errors():
    """
    Adding a main service, with the same name as another service, should error.
    """
    inline = InlineServices()
    inline.add_service('multi_requester', MULTI_REQUESTER_PATH)

    with pytest.raises(ValueError):
        inline.set_main_service(
            'multi_requester',
            MULTI_REQUESTER_PATH
        )


def test_set_main_service_as_module__setting_service_with_same_name_errors():
    """
    Adding a main service, as module, with the same name as another
    service should error.
    """
    inline = InlineServices()
    inline.add_service_by_module(
        'multi_requester',
        import_python_file_from_cwd(MULTI_REQUESTER_PATH)
    )

    with pytest.raises(ValueError):
        inline.set_main_service_by_module(
            'multi_requester',
            import_python_file_from_cwd(MULTI_REQUESTER_PATH)
        )


def test_set_main_service__adding_second_main_service_throws_error():
    """
    Adding a second main service should throw an error.
    """
    inline = InlineServices()
    inline.set_main_service('multi_requester', MULTI_REQUESTER_PATH)

    with pytest.raises(ValueError):
        inline.set_main_service('multi_requester', MULTI_REQUESTER_PATH)


def test_set_main_service_as_module__adding_second_main_service_throws_error():
    """
    Adding a second main service, as module, should throw an error.
    """
    inline = InlineServices()
    inline.add_service_by_module(
        'multi_requester',
        import_python_file_from_cwd(MULTI_REQUESTER_PATH)
    )

    with pytest.raises(ValueError):
        inline.set_main_service_by_module(
            'multi_requester',
            import_python_file_from_cwd(MULTI_REQUESTER_PATH)
        )


def test_start__starting_without_main_service_throws_error():
    """
    Attempting to start an inline service without a main service should throw an error.
    """
    inline = InlineServices()
    inline.add_service('replyer', REPLYER_PATH)

    with pytest.raises(ValueError):
        inline.start()


def test_inline_services__adding_relation_with_improper_out_service_name_throws_error():
    """
    Adding a relation without an output service already added should throw
    an error.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH)

    with pytest.raises(ValueError):
        inline.add_relation('requester', 'request', 'DNE', 'reply')


def test_inline_services__adding_relation_with_improper_in_service_name_throws_error():
    """
    Adding a relation without an input service already added should throw
    an error.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH)

    with pytest.raises(ValueError):
        inline.add_relation('DNE', 'request', 'replyer', 'reply')


def test_inline_services__adding_relation_with_improper_out_connection_name_throws_error():
    """
    Validate the out connection is within the out service.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH)

    with pytest.raises(ValueError):
        inline.add_relation('requester', 'DNE', 'replyer', 'reply')


def test_inline_services__adding_relation_with_improper_in_connection_name_throws_error():
    """
    Validate the in connection is within the in service.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH)

    with pytest.raises(ValueError):
        inline.add_relation('requester', 'request', 'replyer', 'DNE')


def test_get_to_send__to_send_will_only_allow_one_return():
    """
    A single call should not be able to recieve respones from
    multiple sources as the Service Framework is setup to only
    return a single value for each call.
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer_1', REPLYER_PATH)
    inline.add_relation('requester', 'request', 'replyer_1', 'reply')
    inline.add_service('replyer_2', REPLYER_PATH)
    inline.add_relation('requester', 'request', 'replyer_2', 'reply')

    with pytest.raises(RuntimeError):
        inline.start()


def test_get_service_module__happy_case():
    """
    Self Explanitory...
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)
    inline.add_service('replyer', REPLYER_PATH)

    assert inline.get_service_module('requester')
    assert inline.get_service_module('replyer')


def test_get_service_module__service_name_dne_and_throws_error_case():
    """
    Self Explanitory...
    """
    inline = InlineServices()

    with pytest.raises(ValueError):
        inline.get_service_module('requester')


def test_get_service_config__happy_case():
    """
    Self Explanitory...
    """
    inline = InlineServices()
    inline.set_main_service('requester', REQUESTER_PATH)

    config = inline.get_service_config('requester')
    assert 'num_req_to_send' in config


def test_get_service_config__service_name_dne_and_throws_error_case():
    """
    Self Explanitory...
    """
    inline = InlineServices()

    with pytest.raises(ValueError):
        inline.get_service_config('requester')


BASE_DIR = './tests/unit_tests/data/inline_service_integration_test'

DO_NOTHING_PATH = f'{BASE_DIR}/do_nothing_service.py'
REPLYER_PATH = f'{BASE_DIR}/replyer_service.py'
REQUESTER_PATH = f'{BASE_DIR}/requester_service.py'
MULTI_REQUESTER_PATH = f'{BASE_DIR}/multi_requester_service.py'

REQUESTER_CONFIG = {
    'num_req_to_send': 4
}

REPLYER_CONFIG = {
    'response_text': 'NEW_TEXT!'
}
