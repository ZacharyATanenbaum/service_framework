""" Main Function for the Service Framework """

import argparse
from multiprocessing import Process
from service_framework.utils import config_utils, service_utils, utils


def main():
    """
    ~~~ Main Entry to the Framework ~~~
    """
    args, unknown_args = get_arguments()

    config = {}
    if unknown_args:
        print('Getting config from Unknown Args: ', unknown_args)
        config = config_utils.get_config_from_unknown_args(unknown_args)

    print('Getting config from file: ', args.config_path)
    config = {**config, **utils.get_json_from_rel_path(args.config_path)}

    print('Getting Addresses from file: ', args.addresses_path)
    addresses = utils.get_json_from_rel_path(args.addresses_path)

    service = Service(
        args.service_path,
        config=config,
        addresses=addresses,
        console_loglevel=args.console_loglevel,
        log_folder=args.log_folder,
        file_loglevel=args.file_loglevel,
        backup_count=args.backup_count
    )

    if args.main_mode:
        service.run_service_as_main_blocking()
    else:
        service.run_service_blocking()


class Service:
    """
    This class encapsulates the provided service (via service path) and then
    the running of said service in a new subprocess
    """

    def __init__(self,
                 service_path,
                 config=None,
                 addresses=None,
                 console_loglevel='INFO',
                 log_folder=None,
                 file_loglevel='INFO',
                 backup_count=240):
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
        log_folder::str The location of the folder to output logs (if used, None to disable)
        file_loglevel::str The level of the file logger (if used)
        backup_count::int Number of hours that should be saved for file logger
        """
        self.logger_args_dict = {
            'console_loglevel': console_loglevel,
            'log_folder': log_folder,
            'file_loglevel': file_loglevel,
            'backup_count': backup_count
        }

        self.imported_service = utils.import_python_file_from_cwd(service_path)
        self.config = service_utils.setup_config(config, self.imported_service)
        self.addresses = service_utils.setup_addresses(addresses, self.imported_service, config)
        self.connections = service_utils.setup_connections(addresses, self.imported_service, config)
        self.states = service_utils.setup_states(addresses, self.imported_service, config)

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
        if self.process:
            raise RuntimeError('Subprocess is already running!')

        target = service_utils.run_main
        args = (
            self.config,
            self.connections,
            self.states,
            self.imported_service.main,
            self.logger_args_dict
        )
        self._run_target_in_background(target, args)

    def run_service_as_main_blocking(self):
        """
        This method is used to run the service here and block.
        """
        self._setup_sigint_handler()
        service_utils.run_main(
            self.config,
            self.connections,
            self.states,
            self.imported_service.main,
            self.logger_args_dict
        )

    def run_service(self):
        """
        This method is used to encapsulate the running of the service itself.
        """
        if self.process:
            raise RuntimeError('Subprocess is already running!')

        target = service_utils.run_service
        args = (
            self.config,
            self.connections,
            self.states,
            self.logger_args_dict
        )
        self._run_target_in_background(target, args)

    def run_service_blocking(self):
        """
        This method is used to run the service here and block.
        """
        self._setup_sigint_handler()
        service_utils.run_service(
            self.config,
            self.connections,
            self.states,
            self.logger_args_dict
        )

    def _run_target_in_background(self, target, args):
        """
        target::def Function to run in the background.
        args::tuple(obj) Tuple of arguments for the target
        """
        self._setup_sigint_handler()
        self.process = Process(
            target=target,
            args=args
        )
        self.process.daemon = True
        self.process.start()

    def _setup_sigint_handler(self):
        """
        Used to setup the sigint handler when needed.
        """
        service_utils.setup_sigint_handler_func(
            self.imported_service,
            self.config,
            self.connections,
            self.states,
            self.logger_args_dict
        )


def get_arguments():
    """
    This method is needed to get the environmental arguments passed into the system
    as well as setup the config with additionally added environmental arguments.
    return::({}, {}} Known and unknown environment arguments
    """
    parser = argparse.ArgumentParser(description='Run tests on a file.')

    parser.add_argument('-a', '--addresses_path', help='Rel. Loc of the Addresses json')
    parser.add_argument('-c', '--config_path', default=None, help='Relative loc of config json')
    parser.add_argument('-s', '--service_path', help='Relative loc of the service.')
    parser.add_argument('-m', '--main_mode', action='store_true', help='Run as main.')

    parser.add_argument('-cl', '--console_loglevel', default='INFO', help='See name')
    parser.add_argument('-bc', '--backup_count', default=240, help='Num of hourly file backups')
    parser.add_argument('-f', '--file_loglevel', default='INFO', help='See name')
    parser.add_argument('-l', '--log_folder', default=None, help='Log file folder')

    args, unknown_args = parser.parse_known_args()
    print('Using Arguments:', args)
    print('Got unknown Arguments:', unknown_args)
    return args, unknown_args


if __name__ == '__main__':
    main()
