""" Config file functions n'stuff """

import json
import logging
import os

LOG = logging.getLogger(__name__)


def get_config(config_path=None, unknown_args=None):
    """
    Function to parse config file and additional unknown environment arguments.
    config_path::str Relative path to the config file
    unknown_args::[str] ex. ['random_argument', 'HELLO']
    return::{} ex. {**file_arguments, 'random_argument': 'HELLO'}
    """
    LOG.info('Getting Config Info...')
    config = {}

    if config_path:
        config = {**config, **get_config_from_file(config_path)}
    if unknown_args:
        config = {**config, **get_config_from_unknown_args(unknown_args)}

    LOG.info('Returning config info: %s', config)
    return config


def get_config_from_file(config_path):
    """
    Needed to obtain the portion of the config object from a file.
    config_path::str Relative path to the config file
    return::{}
    """
    LOG.info('Getting Config from Relative Path: %s', config_path)
    base_path = os.getcwd()
    absolute_path = os.path.join(base_path, config_path)

    with open(absolute_path, 'r') as config_file:
        config = json.load(config_file)

    LOG.info('Returning Config from Relative Path: %s', config)
    return config


def get_config_from_unknown_args(unknown_args):
    """
    Needed to parse pairs of provided unknown arguments.
    unknown_args::[str] ex. ['random_argument', 'HELLO']
    return::{} ex. {'random_argument': 'HELLO'}
    """
    LOG.info('Getting Config from unknown args: %s', unknown_args)

    if not isinstance(unknown_args, list):
        err = 'Unknown Args MUST come as a list!'
        LOG.error(err)
        raise ValueError(err)

    if len(unknown_args)%2 != 0:
        err = 'Unknown Args MUST come in pairs of two! (As it becomes a dict)'
        LOG.error(err)
        raise ValueError(err)

    config = {}
    unknown_args = iter(unknown_args)

    for key in unknown_args:
        value = next(unknown_args)
        LOG.debug('Adding key, value to config: %s, %s', key, value)
        config[key] = value

    LOG.info('Returning config from Unknown Args: %s', config)
    return config
