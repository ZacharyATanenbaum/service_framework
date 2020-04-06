""" File to house the service class """

from multiprocessing import Process
from service_framework.utils import logging_utils, service_utils, utils


class Service:
    """
    This class encapsulates the provided service (via service path) and then
    the running of said service in a new subprocess
    """

    def __init__(self,
                 service_path,
                 addresses=None,
                 config=None,
                 console_loglevel='INFO',
                 log_path=None,
                 file_loglevel='INFO',
                 backup_count=24):
        """
        service_path = './services/other_folder/service_file.py'
        config = {
            'config_1': 'thingy',
            'config_2': 12345
        }
        addresses = {
            'connections' {
                'in': {
                    'connection_name': {
                        'socket_name': str
                    },
                },
                'out': {},
            },
            'states': {}
        }
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
        logging_utils.setup_package_logger(**self.logger_args_dict)

        self.imported_service = utils.import_python_file_from_cwd(service_path)
        self.config = service_utils.setup_config(config, self.imported_service)
        self.addresses = service_utils.setup_addresses(addresses, self.imported_service, config)
        self.connections = service_utils.setup_service_connections(addresses, self.imported_service, config)
        self.states = service_utils.setup_service_states(addresses, self.imported_service, config)

        service_utils.setup_sigint_handler_func(
            self.imported_service,
            self.config,
            self.connections,
            self.states,
            self.logger_args_dict
        )

        self.process = None

    def __del__(self):
        try:
            if self.process:
                self.process.terminate()
        except AttributeError:
            pass

    def run_service_as_main(self):
        """
        This method is used to encapsulate the running of the service main.
        """
        target = service_utils.run_main
        args = (
            self.imported_service.main,
            self.connections,
            self.states,
            self.config,
            self.logger_args_dict
        )
        self._run_target_in_background(target, args)

    def run_service_as_main_blocking(self):
        """
        This method is used to run the service here and block.
        """
        service_utils.run_main(
            self.imported_service.main,
            self.connections,
            self.states,
            self.config,
            self.logger_args_dict
        )

    def run_service(self):
        """
        This method is used to encapsulate the running of the service itself.
        """
        target = service_utils.run_service
        args = (
            self.connections,
            self.states,
            self.config,
            self.logger_args_dict
        )
        self._run_target_in_background(target, args)

    def run_service_blocking(self):
        """
        This method is used to run the service here and block.
        """
        service_utils.run_service(
            self.connections,
            self.states,
            self.config,
            self.logger_args_dict
        )

    def stop_service(self):
        """
        This method is used to stop a currently running service.
        """
        self.process.terminate()
        self.process = None

    def _run_target_in_background(self, target, args):
        """
        target::def Function to run in the background.
        args::tuple(obj) Tuple of arguments for the target
        """
        if self.process:
            raise RuntimeError('Subprocess is already running!')

        self.process = Process(
            target=target,
            args=args
        )
        self.process.start()
