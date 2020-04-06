""" File to house the Publisher Connection """

from logging import getLogger
import zmq

from service_framework.utils.msgpack_utils import msg_pack
from service_framework.utils.socket_utils import get_publisher_socket
from service_framework.utils.connection_utils import BaseConnection

LOG = getLogger(__name__)


class Publisher(BaseConnection):
    """
    This class is used to send a message to multiple subscribers.
    """
    def __init__(self, model, connection_addresses):
        super().__init__(model, connection_addresses)
        self.connection_addresses = connection_addresses
        self.context = None
        self.model = model
        self.topic = self._setup_topic(model)
        self.socket = None

    def __del__(self):
        if hasattr(self, 'socket'):
            self.socket.close()

    @staticmethod
    def get_addresses_model():
        """
        This is needed so the BaseConnection can validate the
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
            'required_addresses': {'publisher': str},
            'optional_addresses': {},
        }

    @staticmethod
    def get_compatable_connection_types():
        """
        This is needed so the service framework knows which
        connections this current connection is compatable.
        return::['str'] A list of the compatable connections
        """
        return ['subscriber']

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
        return 'publisher'

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
            'optional_creation_arguments': {
                'topic': str,
                'is_x_pub': bool,
                'wait_after_creation_s': float,
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
            'model_function': def(args, to_send, states, conifg) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args),
        }]
        """
        return []

    def runtime_setup(self):
        """
        Method called directly after instantiation to conduct all
        runtime required setup. I.E. Setting up a zmq.Context().
        """
        self.context = zmq.Context()

        self.socket = self._setup_publisher_socket(
            self.connection_addresses['publisher'],
            self.context,
            self.model
        )

    def send(self, payload):
        """
        Method needed for child connection classes to update the state.
        """
        LOG.debug(
            'Attempting to send connection payload "%s" to address "%s" w/ topic "%s"',
            payload,
            self.connection_addresses['publisher'],
            self.topic
        )

        if self.topic:
            to_send = msg_pack(self.topic) + msg_pack(payload)
        else:
            to_send = msg_pack(payload)

        self.socket.send(to_send)
        LOG.debug('Sent payload!')

    @staticmethod
    def _setup_publisher_socket(address, context, model):
        """
        Method is needed to setup the publisher service
        depending on the input arguments.
        address::str ex. 127.0.0.1:9900
        context::zmq.Context
        model = {
            'connection_type': str,
            ...
        }
        """
        opt_args = model.get('optional_creation_arguments', {})
        is_x_pub = opt_args.get('is_x_pub', False)
        wait_after_creation_s = opt_args.get('wait_after_creation_s', 0.15)

        return get_publisher_socket(
            address,
            context,
            is_x_pub=is_x_pub,
            wait_after_creation_s=wait_after_creation_s
        )

    @staticmethod
    def _setup_topic(model):
        """
        This method is needed to setup the topic.
        model = {
            'connection_type': str,
            ...
        }
        """
        opt_args = model.get('optional_creation_arguments', {})
        return opt_args.get('topic', '')
