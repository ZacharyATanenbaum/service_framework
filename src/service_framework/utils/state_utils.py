""" File to house state functions and logic """

from abc import ABC, abstractmethod
import logging

from .validation_utils import validate_args
from .utils import import_python_file_from_module, snake_case_to_capital_case

LOG = logging.getLogger(__name__)


def get_state_update_validator(model):
    """
    model = {
      'state_type': 'local_variable | redshift_database | etc',
      ...
    }
    """
    LOG.info('Creating Validator for Updating a State')

    required_state = model.get('required_state_arguments', {})
    required_arguments = model.get('required_arguments', {})
    required = {**required_state, **required_arguments}

    optional_state = model.get('optional_state_arguments', {})
    optional_arguments = model.get('optional_arguments', {})
    optional = {**optional_state, **optional_arguments}

    def validator(args):
        return validate_args(args, required, optional)
    return validator


def get_state_return_validator(model):
    """
    model = {
      'state_type': 'local_variable | redshift_database | etc',
      ...
    }
    """
    LOG.info('Creating Validator for arguments returned to the State')

    required = model.get('required_return_arguments', {})
    optional = model.get('optional_return_arguments', {})

    def validator(args):
        return validate_args(args, required, optional)
    return validator


def get_state(model, side, state_addresses):
    """
    model = {
      'state_type': 'local_variable | redshift_database | etc',
      ...
    }
    state_addresses::{} A dictionary of the addresses used for this state model.
    return::Base{side}State()
    """
    LOG.info('Creating state for side "%s" and model: %s', side, str(model))
    state_type = model['state_type']
    state_type_class_name = snake_case_to_capital_case(state_type)

    path = 'service_framework.states.{side}.{state_type}'.format(
        side=side,
        state_type=state_type
    )

    state_import = import_python_file_from_module(path)
    state_obj = getattr(state_import, state_type_class_name)

    return state_obj(model, state_addresses)


def setup_states(state_models, addresses):
    """
    state_models = {
        'in': {
            'state_name': {
                'socket_type': 'subscriber | delta | etc',
                ...
            },
        },
        'out': {
            'state_name': {
                'socket_type: 'publisher | delta | etc',
                ...
            },
        },
    }
    addressess = {
        'connections': {},
        'states': {
            'in': {
                'state_name': {
                    'socket_name_1': '127.0.0.1:5001',
                    'socket_name_2': '127.0.0.1:5002',
                },
            },
            'out': {
                'state_name_2': {
                    'socket_name_1': '256.24.52.1:9000',
                },
            },
        },
    }
    return = {
        'in': {
            'state_name': BaseState(),
        },
        'out': {
            'state_name': BaseState(),
        },
    }
    """
    LOG.info('Setting up States...')
    states = {}

    for side in ('in', 'out'):
        LOG.debug('Creating State for Side: %s', side)

        if side not in state_models:
            LOG.debug('Side "%s" not in state_models', side)
            continue

        states[side] = {}

        for model_name, model in state_models[side].items():
            LOG.debug('Creating State for Name %s of Side %s', model_name, side)

            states[side][model_name] = get_state(
                model,
                side,
                addresses['states'][side][model_name]
            )

    LOG.info('Returning States: %s', states)
    return states


def validate_state_model(model):
    """
    model = {
      'state_type': 'subscriber | delta | etc',
      ...
    }
    """
    LOG.info('Validating State Model: %s', model)
    required_fields = [
        'state_type',
    ]
    optional_fields = [
        'required_creation_arguments',
        'optional_creation_arguments',
        'required_state_arguments',
        'optional_state_arguments',
        'required_arguments',
        'optional_arguments',
        'required_return_arguments',
        'optional_return_arguments',
    ]
    validate_args(
        set(model.keys()),
        set(required_fields),
        set(optional_fields)
    )


class BaseState(ABC):
    """
    Framework for creating a new State
    """
    def __init__(self, model, state_addresses):
        """
        model = {
          'state_type': 'local_variable | delta | etc',
          ...
        }
        state_addresses = {
            'socket_name': '127.0.0.1:8001',
            'socket_name_2': '127.0.0.1:8002',
        }
        """
        self.model = model
        self.state_addresses = state_addresses

        validate_state_model(model)
        self._validate_state_addresses(state_addresses)
        self._validate_state_arguments(model)
        self._validate_creation_arguments(model)

        self.args_validator = get_state_update_validator(model)
        self.return_validator = get_state_return_validator(model)

    @staticmethod
    @abstractmethod
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

    @staticmethod
    @abstractmethod
    def get_compatable_state_types():
        """
        This is needed so the service framework knows which
        states this current state is compatable.
        return::['str'] A list of the compatable state, update types.
        """

    @staticmethod
    @abstractmethod
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

    @staticmethod
    @abstractmethod
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

    @staticmethod
    @abstractmethod
    def get_state_type():
        """
        This is needed so the service framework knows the
        state type of the current state.
        return::str The state and update type of this state.
        """

    @abstractmethod
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

    def get_state(self):
        """
        This method is used for the service framework to get the current state.
        return::{}
        """
        LOG.debug('"get_state" not overwritten: %s', self.model)
        return {}

    def send(self, payload):
        """
        Method needed for child classes to modify sending behavior.
        """
        error = f'This State has no send destination... {self.model}'
        LOG.error(error)
        raise RuntimeError(error)

    def _validate_creation_arguments(self, model):
        """
        model = {
          'socket_type': 'subscriber | delta | etc',
          ...
        }
        """
        required_creation_args = model.get('required_creation_arguments', {})
        optional_creation_args = model.get('optional_creation_arguments', {})
        creation_args = {**required_creation_args, **optional_creation_args}

        validate_args(
            creation_args,
            self.get_creation_arguments_model().get('required_creation_arguments', {}),
            self.get_creation_arguments_model().get('optional_creation_arguments', {})
        )

    def _validate_state_addresses(self, state_addresses):
        """
        state_addresses = {
            'socket_name': '127.0.0.1:8001',
            'socket_name_2': '127.0.0.1:8002',
        }
        """
        LOG.info('Validating State Addresses: %s', state_addresses)
        validate_args(
            state_addresses,
            self.get_addresses_model().get('required_addresses', {}),
            self.get_addresses_model().get('optional_addresses', {})
        )

    def _validate_state_arguments(self, model):
        """
        model = {
          'socket_type': 'subscriber | delta | etc',
          ...
        }
        """
        obtained_required_state_args = model.get('required_state_arguments', {})
        obtained_optional_state_args = model.get('optional_state_arguments', {})

        required_state_args = self.get_state_arguments_model().get('required_state_arguments', {})
        optional_state_args = self.get_state_arguments_model().get('optional_state_arguments', {})

        assert obtained_required_state_args == required_state_args
        assert obtained_optional_state_args == optional_state_args

    def __repr__(self):
        return 'State Obj Named: {}, with Model {} and Addresses {}'.format(
            self.__class__.__name__,
            str(self.model),
            str(self.state_addresses)
        )
