""" Holds lots of fun testing utils """

import sys


def remove_imported_object_module(imported_object):
    """
    This method is needed to prevent python from returning the
    cached imported object. Otherwise, if the cached object has changed
    (such as deleting a key in one of the modules local dict variables)
    the next time it is imported the change will persist.
    """
    del sys.modules[imported_object.__name__]
