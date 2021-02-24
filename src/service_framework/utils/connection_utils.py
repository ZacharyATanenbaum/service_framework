""" Holds Different Types of Connection Creation """

from abc import ABC, abstractmethod
import logging

from .validation_utils import validate_args
from .utils import import_python_file_from_module, snake_case_to_capital_case

LOG = logging.getLogger(__name__)


def get_connection_args_validator(model):
    """
    model = {
      'socket_type': 'subscriber | requester | etc',
      ...
    }
    return::def(args) -> raise ValueException
    """
    LOG.debug('Creating Validator for arguments passed to the Connector')

    required_connection_arguments = model.get('required_connection_arguments', {})
    required_arguments = model.get('required_arguments', {})
    required = {**required_connection_arguments, **required_arguments}

    optional_connection_arguments = model.get('optional_connection_arguments', {})
    optional_arguments = model.get('optional_arguments', {})
    optional = {**optional_connection_arguments, **optional_arguments}

    def validator(args):
        return validate_args(args, required, optional)
    return validator


def get_connection_return_validator(model):
    """
    model = {
      'socket_type': 'subscriber | delta | etc',
      ...
    }
    """
    LOG.debug('Creating Validator for arguments returned to the Connector')

    required_return_arguments = model.get('required_return_arguments', {})
    required = {**required_return_arguments}

    optional_return_arguments = model.get('optional_return_arguments', {})
    optional = {**optional_return_arguments}

    def validator(args):
        return validate_args(args, required, optional)
    return validator


def get_connection(model, side, connection_addresses):
    """
    model = {
      'socket_type': 'subscriber | delta | etc',
      ...
    }
    side::('in' | 'out')
    connection_addresses = {
        'socket_name': '127.0.0.1:8001',
        'socket_name_2': '127.0.0.1:8002',
    }
    return::BaseConnection()
    """
    LOG.debug('Creating connection for side "%s" and model: %s', side, str(model))
    connection_type = model['connection_type']
    connection_type_class_name = snake_case_to_capital_case(connection_type)

    module_path = 'service_framework.connections.{side}.{connection_type}'.format(
        side=side,
        connection_type=connection_type
    )

    connection_import = import_python_file_from_module(module_path)
    connection_obj = getattr(connection_import, connection_type_class_name)

    connection = connection_obj(model, connection_addresses)
    connection.runtime_setup()

    return connection


def setup_connections(connection_models, addresses):
    """
    connection_models = {
        'in': {
            'connection_name': {
                'connection_type': 'subscriber | delta | etc',
                ...
            },
        },
        'out': {
            'connection_name': {
                'connection_type: 'publisher | delta | etc',
                ...
            },
        },
    }
    addressess = {
        'connections': {
            'in': {
                'connection_name': {
                    'socket_name_1': '127.0.0.1:5001',
                    'socket_name_2': '127.0.0.1:5002',
                },
            },
            'out': {
                'connection_name': {
                    'socket_name_1': '256.24.52.1:9000',
                },
            },
        },
        'states': {},
    }
    return = {
        'in': {
            'connection_name': BaseConnection()
        }
        'out': {
            'connection_name': BaseConnection()
        },
    }
    """
    LOG.debug('Setting up Connections...')
    conns = {}

    for side in ('in', 'out'):
        LOG.debug('Creating Connections for Side: %s', side)

        if side not in connection_models:
            LOG.debug('Side "%s" not in connection_models', side)
            continue

        conns[side] = {}

        for model_name, model in connection_models[side].items():
            LOG.debug('Creation Conn for Modelname "%s" of Side "%s"', model_name, side)

            connection_addresses = addresses.get('connections', {})
            side_addresses = connection_addresses.get(side, {})
            model_addresses = side_addresses.get(model_name, {})

            if not model_addresses:
                LOG.warning('[connections][%s][%s] NOT IN ADDRESSES FILE!', side, model_name)

            conns[side][model_name] = get_connection(
                model,
                side,
                model_addresses
            )

    LOG.debug('Returning Connections: %s', conns)
    return conns


def validate_connection_model(model):
    """
    model = {
      'connection_type': 'subscriber | delta | etc',
      ...
    }
    """
    LOG.debug('Validating the connection model: %s', model)
    required_fields = [
        'connection_type',
    ]
    optional_fields = [
        'required_creation_arguments',
        'optional_creation_arguments',
        'required_connection_arguments',
        'optional_connection_arguments',
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
    LOG.debug('Connection model passed!')


class BaseConnection(ABC):
    """
    Framework for creating a new Connection
    """
    def __init__(self, model, connection_addresses):
        """
        model = {
          'connection_type': 'subscriber | delta | etc',
          ...
        }
        connection_addresses = {
            'socket_name': '127.0.0.1:8001',
            'socket_name_2': '127.0.0.1:8002',
        }
        """
        self.model = model
        self.connection_addresses = connection_addresses

        validate_connection_model(model)
        self._validate_connection_addresses(connection_addresses)
        self._validate_connection_arguments(model)
        self._validate_creation_arguments(model)

        self.args_validator = get_connection_args_validator(model)
        self.return_validator = get_connection_return_validator(model)

    @staticmethod
    @abstractmethod
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

    @staticmethod
    @abstractmethod
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

    @staticmethod
    @abstractmethod
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

    @abstractmethod
    def get_inbound_sockets_and_triggered_functions(self):
        """
        Method needed so the service framework knows which sockets to listen
        for new messages and what functions to call when a message appears.
        return [{
            'inbound_socket': zmq.Context.Socket,
            'decode_message': def(bytes) -> payload,
            'arg_validator': def(args),
            'connection_function': def(args, to_send, states, config) -> return_args or None,
            'return_validator': def(return_args)
            'return_function': def(return_args),
        }]
        """

    @abstractmethod
    def runtime_setup(self):
        """
        Method called directly after instantiation to conduct all
        runtime required setup. I.E. Setting up a zmq.Context().
        """

    def send(self, payload):
        """
        Method needed for child classes to modify sending
        behavior.
        """
        error = f'This Connector has no send destination... {self.model}'
        LOG.error(error)
        raise RuntimeError(error)

    def _validate_connection_addresses(self, connection_addresses):
        """
        connection_addresses = {
            'socket_name': '127.0.0.1:8001',
            'socket_name_2': '127.0.0.1:8002',
        }
        """
        LOG.debug('Validating Connection Addresses: %s', connection_addresses)
        validate_args(
            connection_addresses,
            self.get_addresses_model().get('required_addresses', {}),
            self.get_addresses_model().get('optional_addresses', {})
        )
        LOG.debug('Validated Connection Addresses!')

    def _validate_connection_arguments(self, model):
        """
        model = {
          'socket_type': 'subscriber | delta | etc',
          ...
        }
        """
        LOG.debug('Validating Model Has Connection Arguments: %s', model)
        obtained_required_connection_args = model.get('required_connection_arguments', {})
        obtained_optional_connection_args = model.get('optional_connection_arguments', {})

        req_args = self.get_connection_arguments_model().get('required_connection_arguments', {})
        opt_args = self.get_connection_arguments_model().get('optional_connection_arguments', {})

        assert obtained_required_connection_args == req_args
        assert obtained_optional_connection_args == opt_args

    def _validate_creation_arguments(self, model):
        """
        model = {
          'socket_type': 'subscriber | delta | etc',
          ...
        }
        """
        LOG.debug('Validating Model Creation Arguments: %s', model)
        required_creation_args = model.get('required_creation_arguments', {})
        optional_creation_args = model.get('optional_creation_arguments', {})
        creation_args = {**required_creation_args, **optional_creation_args}

        validate_args(
            creation_args,
            self.get_creation_arguments_model().get('required_creation_arguments', {}),
            self.get_creation_arguments_model().get('optional_creation_arguments', {})
        )
        LOG.debug('Validated Model Creation Arguments!')

    def __repr__(self):
        return 'Connection Obj Named: {}, with Model {} and Addresses {}'.format(
            self.__class__.__name__,
            str(self.model),
            str(self.connection_addresses)
        )
