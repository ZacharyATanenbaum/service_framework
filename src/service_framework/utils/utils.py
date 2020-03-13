""" Utility Functions for the Service/Test Frameworks """

import importlib
from logging import getLogger
import os
import sys

LOG = getLogger(__name__)


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
