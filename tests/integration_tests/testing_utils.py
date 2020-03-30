""" Holds lots of fun testing utils """

import subprocess
import sys


def get_exec_command_for_python_program(path, with_python=False):
    """
    this is used to take a file and return a list of commands to
    run a python program.
    ex. 'python -m service_framework -s service.py'
    path::str
    with_python::bool If the python interpreter location should be returned
    return::[str]
    """
    exec_line = get_execution_line_for_python_program(path)
    exec_list = parse_execution_line_for_python_program(exec_line)

    if not with_python:
        return exec_list

    python_exec_loc = get_python_execution_path()
    return [python_exec_loc] + exec_list


def get_execution_line_for_python_program(path):
    """
    This is used to get the 'python -m service_framework -s service.py'
    etc line for then running using the subprocess module.
    path::str
    return::str
    """
    with open(path, 'r') as run_replyer_file:
        lines = run_replyer_file.readlines()

    for line in lines:
        if 'python' in line:
            return line

    raise ValueError('Provided file does not have a "python" line!')


def get_python_execution_path():
    """
    Determine the location of the python interpreter being used.
    ex. /home/zach/envs/tcorp/bin/python
    return::str
    """
    python_exec_loc = subprocess.check_output(
        ['which', 'python'],
        universal_newlines=True
    )
    return python_exec_loc.strip()


def parse_execution_line_for_python_program(execution_line):
    """
    Take a line ex. 'python -m service_framework -s service.py' and parse
    it so it can be used by the subprocess module.
    execution_line::str
    return::[str]
    """
    split_line = execution_line.split(' ')

    execution_list = []
    for item in split_line:
        if item:
            cleaned_item = item.strip()
            execution_list.append(cleaned_item)

    return execution_list


def remove_imported_object_module(imported_object):
    """
    This method is needed to prevent python from returning the
    cached imported object. Otherwise, if the cached object has changed
    (such as deleting a key in one of the modules local dict variables)
    the next time it is imported the change will persist.
    """
    del sys.modules[imported_object.__name__]
