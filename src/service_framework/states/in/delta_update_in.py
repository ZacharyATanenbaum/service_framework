""" File to house local variables with full update in state """

from logging import getLogger
import zmq

from service_framework.utils.msgpack_utils import msg_pack, msg_unpack
from service_framework.utils.socket_utils import get_subscriber_socket, get_requester_socket
from service_framework.utils.state_utils import BaseState
from service_framework.utils.update_utils import perform_delta_update

LOG = getLogger(__name__)


class DeltaUpdateIn(BaseState):
    """
    Needed to automatically generate inbound models into actual states to wrap
    inbound state changes.
    """
    def __init__(self, model, state_addresses):
        super().__init__(model, state_addresses)
        self.context = zmq.Context()
        self.current_state = {}
        self.current_num = -1

        self.sub_socket = self._setup_subscriber_socket(
            state_addresses['subscriber'],
            self.context,
            model
        )

        self.req_socket = get_requester_socket(
            state_addresses['requester'],
            self.context
        )

    def __del__(self):
        if hasattr(self, 'sub_socket'):
            self.sub_socket.close()
        if hasattr(self, 'req_socket'):
            self.req_socket.close()

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
                'subscriber': str,
                'requester': str
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
        return ['delta_update_out']

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
                'is_snapshot': bool
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
        return 'delta_update_in'

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
}]
        """
        return [{
            'inbound_socket': self.sub_socket,
            'decode_message': self._decode_message,
            'args_validator': self.args_validator,
            'state_function': self.update_state,
            'model_function': None,
            'return_validator': self.return_validator,
            'return_function': None,
        }]

    def update_state(self, args):
        """
        This method updates the currently contained state.
        args = {}
        """
        LOG.debug('Got args to update state: %s', args)

        if args['is_snapshot']:
            LOG.debug("Got snapshot and updating local state to {args['state']}")
            self.current_state = args['state']
            self.current_num = args['current_num']
            return

        if args['current_num'] < self.current_num:
            LOG.debug(
                'Provided number "%s" less than current number "%s", skipping...',
                args['current_num'],
                self.current_num
            )
            return

        if args['current_num'] != self.current_num + 1:
            LOG.debug(
                'Provided number "%s" not expected num "%s", resetting state...',
                args['current_num'],
                self.current_num + 1
            )
            self._reset_state()
            return

        self.current_num = args['current_num']
        self.current_state = perform_delta_update(self.current_state, args)

    def get_state(self):
        """
        Method needed so the service framework is able to properly set the
        current state.
        return::{} The current state as a dict
        """
        return self.current_state

    def _decode_message(self, binary_message):
        """
        this method is needed to take the binary message from the inbound
        socket and convert it into a payload for the service framework to
        then handle.
        """
        opt_args = self.model.get('optional_creation_arguments', {})
        topic = opt_args.get('topic', '')

        if topic:
            topic_bytes = msg_pack(topic)
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
            'state_type': str,
            ...
        }
        """
        opt_args = model.get('optional_creation_arguments', {})
        topic = opt_args.get('topic', '')

        return get_subscriber_socket(
            address,
            context,
            topic
        )

    def _reset_state(self):
        """
        This method is used to request a new snapshot from the
        delta_update_in state.
        """
        LOG.debug('Resetting State!')
        self.req_socket.send(msg_pack({
            'args': {}
        }))
        response = msg_unpack(self.req_socket.recv())
        LOG.debug('Got new state response: %s', response)
        self.current_num = response['return_args']['current_num']
        self.current_state = response['return_args']['state']
