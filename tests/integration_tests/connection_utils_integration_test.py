""" Integration Test File for service_framework.connection_utils.py """

import logging
import pytest
from service_framework.utils import connection_utils
from service_framework.connections.out.requester import Requester

LOG = logging.getLogger(__name__)


def test_connection_utils__base_connection__valid_validate_addresses_case():
    """
    Make sure the addresses provided to a connection are validated in the base
    connector.
    """
    BasicAddressArgsTestingConnection(
        {'connection_type': 'It honestly does not matter'},
        BASIC_ADDRESSES
    )


def test_connection_utils__base_connection__invalid_validate_addresses_case():
    """
    Make sure the addresses provided to a connection are validated in the base
    connector.
    """
    not_all_required_addresses = {**BASIC_ADDRESSES}
    del not_all_required_addresses['required_connection_1']

    with pytest.raises(ValueError):
        BasicAddressArgsTestingConnection({}, not_all_required_addresses)


def test_connection_utils__base_connection__valid_validate_creation_args_case():
    """
    Make sure the creation arguments provided to a connection are validated in
    the base connector.
    """
    BasicCreationArgsTestingConnection(BASIC_MODEL, {})


def test_connection_utils__base_connection__invalid_validate_creation_args_case():
    """
    Make sure the creation arguments provided to a connection are validated in
    the base connector.
    """
    no_required_args = {**BASIC_MODEL}
    del no_required_args['required_creation_arguments']

    with pytest.raises(ValueError):
        BasicCreationArgsTestingConnection(no_required_args, {})


def test_connection_utils__base_connection__normal_send_function_throws_error():
    """
    Make sure that calling the "send" function without overwriting it will throw
    a Runtime error.
    """
    connector = BasicCreationArgsTestingConnection(BASIC_MODEL, {})

    with pytest.raises(RuntimeError):
        connector.send({})


def test_connection_utils__get_connection__valid_get_replyer_case():
    """
    Test if the get_connection function can make a replyer and a requester
    connection that succeeds.
    """
    requester_address = ADDRESSES['connections']['out']['requester_connection']
    requester_model = CONNECTION_MODELS['out']['requester_connection']

    requester = connection_utils.get_connection(
        requester_model,
        'out',
        requester_address
    )

    assert isinstance(requester, Requester)


def test_connection_utils__setup_connections__valid_get_replyers_case():
    """
    Test if the setup_connections function can make both a replyer and a requester
    connection at the same time.
    """
    connections = connection_utils.setup_connections(CONNECTION_MODELS, ADDRESSES)
    conn_1 = connections['out']['requester_connection']
    conn_2 = connections['out']['requester_connection_2']

    assert isinstance(conn_1, Requester)
    assert isinstance(conn_2, Requester)


class BasicAddressArgsTestingConnection(connection_utils.BaseConnection):
    """
    This connection is strictly used for testing in this file...
    """
    @staticmethod
    def get_addresses_model():
        """
        This is needed so the BaseConnector can validate the
        provided addresses and throw an error if any are missing.
        As well as automatically generate documentation.
        NOTE: types must always be "str"
        return = {
            'required_addresses': {
                'req_address_name_1': str,
                'req_address_name_2': str,
            },
            'optional_addresses': {
                'opt_address_name_1': str,
                'opt_address_name_2': str,
            },
        }
        """
        return {
            'required_addresses': {
                'required_connection_1': str,
                'required_connection_2': str,
            },
            'optional_addresses': {
                'optional_connection_1': str,
                'optional_connection_2': str,
            },
        }

    @staticmethod
    def get_compatable_connection_types():
        """
        This is needed so the build system knows which
        connection types this connection is compatable.
        return::['str'] A list of the compatable socket types.
        """
        return []

    @staticmethod
    def get_connection_arguments_model():
        """
        This is needed so the BaseConnection can validate the provided
        model explicitly states the arguments to be passed on each
        send message.
        return = {
            'required_connection_arguments': {
                'required_connection_arg_1': type,
                'required_connection_arg_2': type,
            },
            'optional_connection_arguments': {
                'optional_connection_arg_1': type,
                'optional_connection_arg_2': type,
            },
        }
        """
        return {
            'required_connection_arguments': {},
            'optional_connection_arguments': {},
        }

    @staticmethod
    def get_connection_type():
        """
        This is needed so the build system knows what
        connection type this connection is considered.
        return::str The socket type of this connection.
        """
        return 'basic'

    @staticmethod
    def get_creation_arguments_model():
        """
        This is needed so the BaseConnection can validate the provided
        creation arguments as well as for auto documentation.
        return = {
            'required_creation_arguments': {
                'required_creation_arg_1': type,
                'required_creation_arg_2': type,
            },
            'optional_creation_arguments': {
                'optional_creation_arg_1': type,
                'optional_creation_arg_2': type,
            },
        }
        """
        return {
            'required_creation_arguments': {},
            'optional_creation_arguments': {},
        }

    def get_inbound_sockets_and_triggered_functions(self):
        """
        Method needed so the service framework knows which sockets to listen
        for new messages and what functions to call when a message appears.
        return [{
            'inbound_socket': zmq.Context.Socket,
            'arg_validator': def(args),
            'connection_function': def(args) -> args or None,
            'model_function': def(args, to_send, states, config) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args),
        }]
        """
        return []

    def runtime_setup(self):
        """
        This method is used for the state to do any setup that must occur during
        runtime. I.E. setting up a zmq.Context.
        """


class BasicCreationArgsTestingConnection(connection_utils.BaseConnection):
    """
    This connection is strictly used for testing in this file...
    """
    @staticmethod
    def get_addresses_model():
        """
        This is needed so the BaseConnector can validate the
        provided addresses and throw an error if any are missing.
        As well as automatically generate documentation.
        NOTE: types must always be "str"
        return = {
            'required_addresses': {
                'req_address_name_1': str,
                'req_address_name_2': str,
            },
            'optional_addresses': {
                'opt_address_name_1': str,
                'opt_address_name_2': str,
            },
        }
        """
        return {
            'required_addresses': {},
            'optional_addresses': {},
        }

    @staticmethod
    def get_compatable_connection_types():
        """
        This is needed so the build system knows which
        connection types this connection is compatable.
        return::['str'] A list of the compatable socket types.
        """
        return []

    @staticmethod
    def get_connection_arguments_model():
        """
        This is needed so the BaseConnection can validate the provided
        model explicitly states the arguments to be passed on each
        send message.
        return = {
            'required_connection_arguments': {
                'required_connection_arg_1': type,
                'required_connection_arg_2': type,
            },
            'optional_connection_arguments': {
                'optional_connection_arg_1': type,
                'optional_connection_arg_2': type,
            },
        }
        """
        return {
            'required_connection_arguments': {},
            'optional_connection_arguments': {},
        }

    @staticmethod
    def get_connection_type():
        """
        This is needed so the build system knows what
        connection type this connection is considered.
        return::str The socket type of this connection.
        """
        return 'basic'

    @staticmethod
    def get_creation_arguments_model():
        """
        This is needed so the BaseConnection can validate the provided
        creation arguments as well as for auto documentation.
        return = {
            'required': {
                'required_creation_arg_1': type,
                'required_creation_arg_2': type,
            },
            'optional': {
                'optional_creation_arg_1': type,
                'optional_creation_arg_2': type,
            },
        }
        """
        return {
            'required_creation_arguments': {
                'required_creation_argument_1': str,
                'required_creation_argument_2': int,
            },
            'optional_creation_arguments': {
                'optional_creation_argument_1': str,
                'optional_creation_argument_2': int,
            },
        }

    def get_inbound_sockets_and_triggered_functions(self):
        """
        Method needed so the service framework knows which sockets to listen
        for new messages and what functions to call when a message appears.
        return [{
            'inbound_socket': zmq.Context.Socket,
            'arg_validator': def(args),
            'connection_function': def(args) -> args or None,
            'model_function': def(args, to_send, states, config) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args),
        }]
        """
        return []

    def runtime_setup(self):
        """
        This method is used for the state to do any setup that must occur during
        runtime. I.E. setting up a zmq.Context.
        """


ADDRESSES = {
    'connections': {
        'out': {
            'requester_connection': {
                'requester': '127.0.0.1:8877',
            },
            'requester_connection_2': {
                'requester': '127.0.0.1:8877',
            },
        }
    }
}


CONNECTION_MODELS = {
    'out': {
        'requester_connection': {
            'connection_type': 'requester',
        },
        'requester_connection_2': {
            'connection_type': 'requester',
        },
    },
}


BASIC_ADDRESSES = {
    'required_connection_1': 'req_string_address_1',
    'required_connection_2': 'req_string_address_2',
    'optional_connection_1': 'opt_string_address_1',
    'optional_connection_2': 'opt_string_address_2',
}


BASIC_MODEL = {
    'connection_type': 'basic',
    'required_creation_arguments': {
        'required_creation_argument_1': 'foo',
        'required_creation_argument_2': 7888,
    },
    'optional_creation_arguments': {
        'optional_creation_argument_1': 'bar',
        'optional_creation_argument_2': 1337,
    },
}
