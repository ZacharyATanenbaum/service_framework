""" File to house a Replyer Connection """

from logging import getLogger
import zmq

from service_framework.utils.connection_utils import BaseConnection
from service_framework.utils.msgpack_utils import msg_pack, msg_unpack
from service_framework.utils.socket_utils import get_replyer_socket

LOG = getLogger(__name__)


class Replyer(BaseConnection):
    """
    Needed to automatically generate inbound models into actual connection to wrap
    inbound connections.
    """
    def __init__(self, model, addresses):
        super().__init__(model, addresses)
        self.addresses = addresses
        self.model = model
        self.context = None

        self.on_new_req = model['required_creation_arguments']['on_new_request']
        self.socket = None

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
            'required_addresses': {'replyer': str},
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
            'required_creation_arguments': {
                'on_new_request': lambda args, to_send, states, config: True,
            },
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
        return [{
            'inbound_socket': self.socket,
            'decode_message': self.decode_message,
            'args_validator': self.args_validator,
            'connection_function': None,
            'model_function': self.on_new_req,
            'return_validator': self.return_validator,
            'return_function': self.return_to_requester,
        }]

    def runtime_setup(self):
        """
        Method called directly after instantiation to conduct all
        runtime required setup. I.E. Setting up a zmq.Context().
        """
        self.context = zmq.Context()

        self.socket = get_replyer_socket(
            self.addresses['replyer'],
            self.context
        )

    @staticmethod
    def decode_message(binary_message):
        """
        Method used to take the obtained binary message from req socket and
        convert it into a payload.
        """
        return msg_unpack(binary_message)

    def return_to_requester(self, payload):
        """
        This method is passed with the socket for when a new message is recieved
        for the replyer socket.
        """
        LOG.debug('Sending Return Payload...')
        self.socket.send(msg_pack(payload))
