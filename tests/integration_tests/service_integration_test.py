""" File that houses all of the integration tests for the Service class """

from service_framework import Service

BASE_DIR = './tests/integration_tests'

DO_NOTHING_PATH = f'{BASE_DIR}/data/service_integration_test/do_nothing_service.py'
REPLYER_PATH = f'{BASE_DIR}/data/service_integration_test/replyer_service.py'
REQUESTER_PATH = f'{BASE_DIR}/data/service_integration_test/requester_service.py'

REPLYER_ADDRS = {
    "connections": {
        "in": {
            "reply": {
                "replyer": "127.0.0.1:18900"
            }
        }
    }
}

REQUESTER_ADDRS = {
    "connections": {
        "out": {
            "request": {
                "requester": "127.0.0.1:18900"
            }
        }
    }
}

REQUESTER_CONFIG = {
    'num_req_to_send': 1
}


def test_service__init__service_can_be_constructed_with_just_service_path():
    """
    Make sure the only thing the Service Class needs is a service_path.
    """
    service = Service(DO_NOTHING_PATH)
    service.run_service()
    service.stop_service()


def test_service__init__file_log_functions_properly():
    """
    Make sure the file loglevel and log folder function properly.
    """
    requester = Service(
        REQUESTER_PATH,
        addresses=REQUESTER_ADDRS,
        config=REQUESTER_CONFIG,
        log_path=f'{BASE_DIR}/logs/requester.log',
        file_loglevel='DEBUG'
    )
    replyer = Service(
        REPLYER_PATH,
        addresses=REPLYER_ADDRS,
        log_path=f'{BASE_DIR}/logs/replyer.log',
        file_loglevel='DEBUG'
    )

    replyer.run_service()
    requester.run_service()

    import time
    time.sleep(1)

    raise RuntimeError()



def test_service__del__make_sure_service_cleans_up_properly():
    """
    Make sure that if the service is killed there won't be any
    hanging processes.
    """


def test_service__run_service_as_main__success_case():
    """
    Make sure that the service will run the main method, in
    the background, properly.
    """


def test_service__run_service_as_main_blocking__sucess_case():
    """
    Make sure that the service will run the main method,
    as a blocking process, properly.
    """


def test_service__run_service__success_case():
    """
    Make sure the service will run as an event processing system
    in the background, properly.
    """


def test_service__run_service_blocking__success_case():
    """
    Make sure the service will run as en event processing system
    properly.
    """


def test_service__stop_service__main_success_case():
    """
    Make sure that if running as main in the background the service
    can be programmatically stopped.
    """


def test_service__stop_service__regular_service_success_case():
    """
    Make sure that if running in the background the service can
    be programmatically stopped.
    """


def test_service__setup_sigint_handler__run_target_in_background_case():
    """
    Make sure that if a service is run in the background it will
    still append to the sigint handler.
    """


def test_service__setup_sigint_handler__main_blocking_case():
    """
    Make sure that if a service is run as main and is blocking
    the sigint handler will be appeneded.
    """


def test_service__setup_sigint_handler__service_blocking_case():
    """
    Make sure that if a service is run and it is blocking the sigint
    handler will be appened.
    """
