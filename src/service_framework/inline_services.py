""" File to house the inline services class """

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
        self.configs = {}
        self.main_service = None
        self.services = {}
        self.relations = {}

    def add_relation(self, out_service_name, out_connection, in_service_name, in_connection):
        """
        Add a relation where if the out service_name's out_connection is called all
        in_service_name and in_connection functions will be called.
        out_service_name::str Name of the outbound connection's service
        out_connection::str Name of the outbound connection
        in_service_name::str Name of the inbound connection's service
        in_connection::str Name of the inbound connection
        """
        key = self._get_relation_key(out_service_name, out_connection)

        if key in self.relations:
            self.relations[key] = (in_service_name, in_connection)
        else:
            self.relations[key] = [(in_service_name, in_connection)]

    def add_service(self, service_name, rel_service_path, config=None):
        """
        Add a service to the inline service object. This service will be called if a relation is
        set to call it.
        service_name::str Name of the service to be used for relations
        rel_service_path::str The relative path to the service from the cwd
        config::{} The service config passed to the service
        """
        self.add_service_by_module(
            service_name,
            import_python_file_from_cwd(rel_service_path),
            config
        )

    def add_service_by_module(self, service_name, service_module, config=None):
        """
        Add a service to the inline service object. This service will be called if a relation is
        set to call it.
        service_name::str The name of the service to be used for relations
        service_module::str The imported service file
        config::{} The service config passed to the service
        """
        self._setup_service(service_name, service_module, config)

    def start(self):
        """
        Start the inline service
        """
        # TODO

    def set_main_service(self, service_name, rel_service_path, config=None):
        """
        Add the main service to be used. This service will be the initially called service within
        the inline service function.
        service_name::str The name of the service to be used for relations
        rel_service_path::str The relative path to the service from the cwd
        config::{} The service config passed to the service
        """
        self.set_main_service_by_module(
            service_name,
            import_python_file_from_cwd(rel_service_path),
            config
        )

    def set_main_service_by_module(self, service_name, service_module, config=None):
        """
        Add the main service to be used. This service will be the initially called service within
        the inline service function.
        service_name::str The name of the service to be used for relations
        service_module::str The imported service file
        config::{} The service config passed to the service
        """
        if self.main_service:
            raise ValueError(f'Main Service Already Set as "{self.main_service}"!')
        self.main_service = service_name
        self._setup_service(service_name, service_module, config)

    @staticmethod
    def _get_relation_key(out_service_name, out_connection):
        """
        Create the key used for getting the inbound connections for the
        provided outbound service and connection pair.
        """
        return (out_service_name, out_connection)

    def _setup_service(self, service_name, service_module, config=None):
        """
        Run all the fuctions needed to setup the service.
        service_name::str The name of the service to be used for relations
        service_module::str The imported service file
        config::{} The service config passed to the service
        """
        if service_name in self.services:
            raise ValueError('Service named "{service_name}" already exists! Choose a new name')

        self.services[service_name] = service_module
        self.configs[service_name] = config
