""" File to house the subscriber connection """

from logging import getLogger
import zmq

from service_framework.utils.msgpack_utils import msg_pack, msg_unpack
from service_framework.utils.socket_utils import get_subscriber_socket
from service_framework.utils.connection_utils import BaseConnection

LOG = getLogger(__name__)


class Subscriber(BaseConnection):
    """
    This class is needed to allow a subscriber socket to function
    with the service framework.
    """
    def __init__(self, model, connection_addresses):
        super().__init__(model, connection_addresses)
        self.connection_addressses = connection_addresses
        self.context = None
        self.model = model
        self.socket = None

    def __del__(self):
        if hasattr(self, 'socket'):
            self.socket.close()

    @staticmethod
    def get_addresses_model():
        """
        This is needed so the BaseState can validate the
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
            'required_addresses': {'subscriber': str},
            'optional_addresses': {},
        }

    @staticmethod
    def get_compatable_connection_types():
        """
        This is needed so the build system knows which
        connection types this connection is compatable.
        return::['str'] A list of the compatable socket types.
        """
        return ['publisher']

    @staticmethod
    def get_connection_arguments_model():
        """
        This is needed so the BaseConnection can validate the provided
        model explicitly state the arguments to be passed on each
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
        return 'subscriber'

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
                'connection_function': lambda args, to_send, config: True,
            },
            'optional_creation_arguments': {
                'is_binder': bool,
                'topic': str
            },
        }

    def get_inbound_sockets_and_triggered_functions(self):
        """
        Method needed so the service framework knows which sockets to listen
        for new messages and what functions to call when a message appears.
        return [{
            'inbound_socket': zmq.Context.Socket,
            'decode_message': def(bytes) -> payload,
            'args_validator': def(args),

            'connection_function': def(args) -> args or None,
            'model_function': def(args, to_send, conifg) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args),
        }]
}]
        """
        return [{
            'inbound_socket': self.socket,
            'decode_message': self._decode_message,
            'args_validator': self.args_validator,
            'connection_function': None,
            'model_function': self.model['required_creation_arguments']['on_new_message'],
            'return_validator': None,
            'return_function': None,
        }]

    def runtime_setup(self):
        """
        Method called directly after instantiation to conduct all
        runtime required setup. I.E. Setting up a zmq.Context().
        """
        self.context = zmq.Context()

        self.socket = self._setup_subscriber_socket(
            self.connection_addresses['subscriber'],
            self.context,
            self.model
        )

    def _decode_message(self, binary_message):
        """
        this method is needed to take the binary message from the inbound
        socket and convert it into a payload for the service framework to
        then handle.
        """
        opt_args = self.model.get('optional_creation_arguments', {})
        topic = opt_args.get('topic', '')
        topic_bytes = msg_pack(topic)

        if topic:
            msg_only = binary_message[len(topic_bytes):]
            return msg_unpack(msg_only)

        return msg_unpack(binary_message)

    @staticmethod
    def _setup_subscriber_socket(address, context, model):
        """
        Method is needed to setup the subscriber service
        depending on the input arguments.
        address::str ex. 127.0.0.1:9900
        context::zmq.Context
        model = {
            'connection_type': str,
            ...
        }
        """
        opt_args = model.get('optional_creation_arguments', {})
        topic = opt_args.get('topic', '')

        return get_subscriber_socket(
            address,
            context,
            topic,
            is_binder=opt_args.get('is_binder', False)
        )
