""" Utility Functions for the Service/Test Frameworks """

import importlib
import json
from logging import getLogger
import os
import signal
import sys

LOG = getLogger(__name__)


def add_sigint_handler(new_handler_func):
    """
    Wraps setting the sigint handler to properly set the handler without
    overwriting the original sigint handler.
    func::def(signum, frame) Function to set the new handler
    """
    previous_handler = signal.getsignal(signal.SIGINT)

    def new_sigint_handler(sigint, frame):
        new_handler_func(sigint, frame)
        previous_handler(sigint, frame)

    signal.signal(signal.SIGINT, new_sigint_handler)


def convert_path_to_import(path):
    """
    path::str Path to a file
    return::str Import string for the same file
    """
    LOG.info('Converting Path to Import Statement: %s', path)
    if len(path) > 3 and path[:2] == './':
        path = path[2:]

    if '/../' in path:
        path = path.replace('/../', '..')

    if '../' in path:
        path = path.replace('../', '..')

    path = path[:-3] # Remove .py from path
    import_statement = path.replace('/', '.')

    LOG.info('Returning Import Statement: %s', import_statement)
    return import_statement


def get_json_from_rel_path(rel_path):
    """
    rel_path::str The relative path to the json file
    """
    if not rel_path:
        return {}

    with open(rel_path, 'r') as file_to_import:
        return json.load(file_to_import)


def import_python_file_from_cwd(path):
    """
    path::str Path to a file (ex. './folder/folder_1/filename.py')
    return::Object The imported Python file
    """
    LOG.info('Importing Python File from: %s', path)
    import_path = convert_path_to_import(path)
    sys.path.append(os.getcwd())
    imported_module = importlib.import_module(import_path)
    LOG.info('Returning Imported Module: %s', import_path)
    return imported_module


def import_python_file_from_module(module_path):
    """
    module_path::str Path to file in module (ex. 'module_name.folder.file')
    return::Object The imported Python file
    """
    LOG.info('Importing File from Module Path: %s', module_path)
    imported_module = importlib.import_module(module_path)
    LOG.info('Returning Imported Module: %s', module_path)
    return imported_module


def snake_case_to_capital_case(string):
    """
    string::str ex. this_is_an_example
    return::str ex. ThisIsAnExample
    """
    LOG.info('Converting string to capital case: %s', string)
    split_list = string.split('_')
    capital_list = [item.capitalize() for item in split_list]
    capital_case = ''.join(capital_list)
    LOG.info('Returning captial case: %s', capital_case)
    return capital_case
