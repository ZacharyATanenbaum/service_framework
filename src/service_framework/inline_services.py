""" File to house the inline services class """

from service_framework.utils import service_utils
from service_framework.utils.utils import import_python_file_from_cwd


class InlineServices:
    """
    This class encompasses the framework to properly inline services.
    Instead of running services across multiple threads or processes
    this class will run them inline on one thread. Cutting out the
    connectivity behavior and greatly increasing the efficiency of
    the code.
    """

    def __init__(self,
                 console_loglevel='INFO',
                 log_path=None,
                 file_loglevel='INFO',
                 backup_count=24):
        """
        console_loglevel::str Level of the console logger (if used, None to disable)
        log_path::str The location of the folder to output logs (if used, None to disable)
        file_loglevel::str The level of the file logger (if used)
        backup_count::int Number of hours that should be saved for file logger
        """
        self.logger_args_dict = {
            'console_loglevel': console_loglevel,
            'log_path': log_path,
            'file_loglevel': file_loglevel,
            'backup_count': backup_count
        }
        self.main_service = None
        self.services = {}

    def add_relation(self, out_service_name, out_connection, in_service_name, in_connection):
        pass

    def add_service(self, service_name, rel_service_path):
        """
        Add a service to the inline service object. This service will be called if a relation is
        set to call it.
        service_name::str Name of the service to be used for relations
        rel_service_path::str The relative path to the service from the cwd
        """
        self.add_service_by_module(service_name, import_python_file_from_cwd(rel_service_path))

        if service_name in self.services:
            raise ValueError('Service named "{service_name}" already exists! Please choose a new name')

    def add_service_by_module(self, service_name, service_module):
        pass

    def start(self):
        pass

    def set_main_service(self, service_name, rel_service_path):
        """
        Add the main service to be used. This service will be the initially called service within
        the inline service function.
        service_name::str The name of the service to be used for relations
        rel_service_path::str The relative path to the service from the cwd
        """
        self.set_main_service_by_module(service_name, import_python_file_from_cwd(rel_service_path))

    def set_main_service_by_module(self, service_name, service_module):
        pass
