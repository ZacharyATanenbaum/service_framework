""" File to house validation functions """

from inspect import signature
import logging
from types import FunctionType

LOG = logging.getLogger(__name__)


def validate_args(new_args, required_args, optional_args):
    """
    new_args::{set, dict}
    required_args::{set, dict}
    optional_args::{set, dict}
    """
    LOG.debug('NEW ARGS %s, REQUIRED %s, OPTIONAL %s', new_args, required_args, optional_args)

    if isinstance(new_args, dict):
        validate_required_arg(new_args, required_args)
        non_required_keys = new_args.keys() - required_args.keys()
        non_required_args = {key: val for key, val in new_args.items() if key in non_required_keys}
        validate_optional_arg(non_required_args, optional_args)

    elif isinstance(new_args, set):
        validate_required_arg(new_args, required_args)
        non_required_args = new_args - required_args
        validate_optional_arg(non_required_args, optional_args)

    else:
        err = 'Attempting to validate unsupported type: {}'.format(type(new_args))
        LOG.error(err)
        raise ValueError(err)


def validate_optional_arg(non_required_arg, optional_type):
    """
    Make sure arguments passed are defined as optional args.
    non_required_arg::obj
    optional_type::obj
    """
    LOG.debug('non_required_arg: %s, optional_type: %s', non_required_arg, optional_type)
    if isinstance(non_required_arg, dict):
        for key, val in non_required_arg.items():
            if key not in optional_type:
                err = 'Key "{}" not in optional arguments "{}"'.format(
                    key,
                    optional_type
                )
                LOG.error(err)
                raise ValueError(err)

            validate_optional_arg(val, optional_type[key])

    elif isinstance(non_required_arg, list):
        for item in non_required_arg:
            validate_optional_arg(item, optional_type[0])

    elif isinstance(non_required_arg, tuple):
        if len(non_required_arg) != len(optional_type):
            err = 'Provided non-required tuple "{}" not same size as optional "{}"'.format(
                non_required_arg,
                optional_type
            )
            LOG.error(err)
            raise ValueError(err)

        for idx, item in enumerate(non_required_arg):
            current_optional_type = optional_type[idx]
            validate_optional_arg(item, current_optional_type)

    elif (isinstance(non_required_arg, set)
          and isinstance(optional_type, set)
          and len(optional_type) == 1
          and isinstance(next(iter(optional_type)), type)):
        # Make sure, if given a set of a single value, that each argument of the provided set is
        # of that type.
        #
        # ex. non_required_args = {'test', 'test2'} optional_type = {str}
        # This example would be valid...
        for item in non_required_arg:
            validate_optional_arg(item, next(iter(optional_type)))

    elif isinstance(non_required_arg, set):
        # Make sure, if given a set of values, that each non_required_argument is of that set.
        #
        # ex. non_required_args = {'test', 'test2'} optional_type = {'test', 'test2', 'test3'}
        # This example would be valid....
        for item in non_required_arg:
            if item not in optional_type:
                err = 'Provided item "{}" of set "{}" is not in optional set "{}"'.format(
                    item,
                    non_required_arg,
                    optional_type
                )
                LOG.error(err)
                raise ValueError(err)

    elif isinstance(non_required_arg, FunctionType) and isinstance(optional_type, FunctionType):
        non_required_arg_signature = signature(non_required_arg)
        optional_type_signature = signature(optional_type)

        if non_required_arg_signature != optional_type_signature:
            err = 'Provided func "{}" with signature "{}" missing optional signature "{}"'.format(
                non_required_arg,
                non_required_arg_signature,
                optional_type_signature
            )
            LOG.error(err)
            raise ValueError(err)

    elif not isinstance(non_required_arg, optional_type):
        err = 'Non Required Argument "{}" type "{}" is not of optional type "{}"'.format(
            non_required_arg,
            type(non_required_arg),
            optional_type
        )
        LOG.error(err)
        raise ValueError(err)


def validate_required_arg(new_arg, required_type):
    """
    Make sure required arguments are present.
    new_arg::obj
    required_type::obj
    return::bool
    """
    LOG.debug('new_arg: %s, required_type: %s', new_arg, required_type)
    if isinstance(required_type, dict):
        for key, val in required_type.items():
            if key not in new_arg:
                err = 'Key "{}" not in new arg "{}"'.format(key, new_arg)
                LOG.error(err)
                raise ValueError(err)

            validate_required_arg(new_arg[key], val)

    elif isinstance(required_type, list):
        for item in new_arg:
            validate_required_arg(item, required_type[0])

    elif isinstance(required_type, tuple):
        if len(required_type) != len(new_arg):
            err = 'Provided tuple argument "{}" not same size as required "{}"'.format(
                new_arg,
                required_type
            )
            LOG.error(err)
            raise ValueError(err)

        for idx, item in enumerate(new_arg):
            current_required_type = required_type[idx]
            validate_required_arg(item, current_required_type)

    elif (isinstance(required_type, set)
          and len(required_type) == 1
          and isinstance(next(iter(required_type)), type)):
        # Make sure that each new_args in the set if of the required set's type.
        #
        # ex. required_type = {str} new_args = {'test', 'test2'}
        # This example would be valid...
        for arg in new_arg:
            validate_optional_arg(arg, next(iter(required_type)))

    elif isinstance(required_type, set):
        # Make sure, if given a set of values, that each value is of the required set
        #
        # ex. required_type = {'test', 'test2'} new_args = {'test', 'test2'}
        # This example would be valid....
        for item in required_type:
            if item not in new_arg:
                err = 'item "{}" of required set "{}" not found in set "{}"'.format(
                    item,
                    required_type,
                    new_arg
                )
                LOG.error(err)
                raise ValueError(err)

    elif isinstance(new_arg, FunctionType) and isinstance(required_type, FunctionType):
        new_arg_signature = signature(new_arg)
        required_type_signature = signature(required_type)

        if new_arg_signature != required_type_signature:
            err = 'Provided func "{}" with signature "{}" misisng required signature "{}"'.format(
                new_arg,
                new_arg_signature,
                required_type_signature
            )
            LOG.error(err)
            raise ValueError(err)

    elif not isinstance(new_arg, required_type):
        err = 'New Argument "{}" of type "{}" is not of required type "{}"'.format(
            new_arg,
            type(new_arg),
            required_type
        )
        LOG.error(err)
        raise ValueError(err)
