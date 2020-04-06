""" File to house the state LocalVariablesWithFullUpdateOut """

import zmq

from service_framework.utils.logging_utils import get_logger
from service_framework.utils.msgpack_utils import msg_pack, msg_unpack
from service_framework.utils.socket_utils import get_publisher_socket, get_replyer_socket
from service_framework.utils.state_utils import BaseState
from service_framework.utils.update_utils import perform_delta_update

LOG = get_logger()


class DeltaUpdateOut(BaseState):
    """
    This class is needed to partially update the local variable state.
    """
    def __init__(self, model, state_addresses):
        super().__init__(model, state_addresses)
        self.context = None
        self.model = model
        self.state_addresses = state_addresses
        self.topic = self._setup_topic(model)
        self.current_state = {}
        self.current_num = 0

        self.pub_socket = None
        self.rep_socket = None

    def __del__(self):
        if hasattr(self, 'pub_socket') and self.pub_socket:
            self.pub_socket.close()
        if hasattr(self, 'rep_socket') and self.rep_socket:
            self.rep_socket.close()

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
            'required_addresses': {
                'publisher': str,
                'replyer': str,
            },
            'optional_addresses': {},
        }

    @staticmethod
    def get_compatable_state_types():
        """
        This is needed so the service framework knows which
        states this current state is compatable.
        return::['str'] A list of the compatable state, update types.
        """
        return ['delta_update_in']

    @staticmethod
    def get_creation_arguments_model():
        """
        This is needed so the BaseState can validate the provided
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

    @staticmethod
    def get_state_arguments_model():
        """
        This is needed so the BaseState can validate the provided
        model has the required or optional arguments for the state
        to function.
        return = {
            'required_state_arguments': {
                'required_state_arg_1': type,
                'required_state_arg_2': type,
            },
            'optional_state_arguments': {
                'optional_state_arg_1': type,
                'optional_state_arg_2': type,
            },
        }
        """
        return {
            'required_state_arguments': {
                'current_num': int,
                'is_snapshot': bool,
            },
            'required_State_arguments': {},
        }

    @staticmethod
    def get_state_type():
        """
        This is needed so the service framework knows the
        state type of the current state.
        return::str The state and update type of this state.
        """
        return 'delta_update_out'

    def get_inbound_sockets_and_triggered_functions(self):
        """
        Method needed so the service framework knows which sockets to listen
        for new messages and what functions to call when a message appears.
        return [{
            'inbound_socket': zmq.Context.Socket,
            'decode_message': def(bytes) -> payload,
            'args_validator': def(args),
            'state_function': def(args) -> args or None,
            'model_function': def(args, to_send, states, conifg) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args),
        }]
        """
        return [{
            'inbound_socket': self.rep_socket,
            'decode_message': self._decode_message,
            'args_validator': None,
            'state_function': self._get_current_state,
            'model_function': None,
            'return_validator': None,
            'return_function': self._return_to_requester,
        }]

    def _get_current_state(self, _):
        """
        Get the entire current state and return it.
        """
        return {
            'state': self.current_state,
            'current_num': self.current_num,
        }

    def runtime_setup(self):
        """
        This method is used for the state to do any setup that must occur during
        runtime. I.E. setting up a zmq.Context.
        """
        self.context = zmq.Context()

        self.pub_socket = self._setup_publisher_socket(
            self.state_addresses['publisher'],
            self.context,
            self.model
        )

        self.rep_socket = get_replyer_socket(
            self.state_addresses['replyer'],
            self.context
        )

    def send(self, payload):
        """
        Method needed for child state classes to update the state.
        """
        LOG.debug(
            'Attempting to send state payload "%s" to address "%s" w/ topic "%s"',
            payload,
            self.state_addresses['publisher'],
            self.topic
        )

        if payload['args']['is_snapshot']:
            self.current_state = payload['args']['state']
        else:
            self.current_state = perform_delta_update(self.current_state, payload['args'])

        if self.topic:
            to_send = msg_pack(self.topic) + msg_pack(payload)
        else:
            to_send = msg_pack(payload)

        self.pub_socket.send(to_send)
        LOG.debug('Sent payload!')

    @staticmethod
    def _setup_publisher_socket(address, context, model):
        """
        Method is needed to setup the publisher service
        depending on the input arguments.
        address::str ex. 127.0.0.1:9900
        context::zmq.Context
        model = {
            'state_type': str,
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
            'state_type': str,
            ...
        }
        """
        opt_args = model.get('optional_creation_arguments', {})
        return opt_args.get('topic', '')

    @staticmethod
    def _decode_message(binary_message):
        """
        Method used to take the obtained binary message from req socket and
        convert it into a payload.
        """
        return msg_unpack(binary_message)

    def _return_to_requester(self, payload):
        """
        This method is passed with the socket for when a new message is recieved
        for the replyer socket.
        """
        LOG.debug('Sending Return Payload...')
        self.rep_socket.send(msg_pack(payload))
