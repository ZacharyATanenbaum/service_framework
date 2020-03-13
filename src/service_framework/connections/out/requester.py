""" File to house a requester connection """

from logging import getLogger
import zmq

from service_framework.utils.connection_utils import BaseConnection
from service_framework.utils.msgpack_utils import msg_pack, msg_unpack
from service_framework.utils.socket_utils import get_requester_socket

LOG = getLogger(__name__)


class Requester(BaseConnection):
    """
    Needed to automatically generate all connection functions/sockets so external
    calls will be properly handled.
    """
    def __init__(self, model, addresses):
        super().__init__(model, addresses)
        self.context = zmq.Context()

        self.socket = get_requester_socket(
            addresses['requester'],
            self.context
        )

    def __del__(self):
        if hasattr(self, 'socket'):
            self.socket.close()

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
            'required_addresses': {'requester': str},
            'optional_addresses': {},
        }

    @staticmethod
    def get_compatable_connection_types():
        """
        This is needed so the build system knows which
        connection types this connection is compatable.
        return::['str'] A list of the compatable socket types.
        """
        return ['requester']

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
        return 'replyer'

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
            'decode_message': def(bytes) -> payload,
            'arg_validator': def(args),
            'connection_function': def(args) -> args or None,
            'model_function': def(args, to_send, states, conifg) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args),
        }]
        """
        return []

    def send(self, payload):
        """
        This is needed to wrap socket calls. So all calls to the connection
        will be properly formatted.
        """
        self.socket.send(msg_pack(payload))
        return msg_unpack(self.socket.recv())
