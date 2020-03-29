""" Main Function for the Service Framework """

import argparse
from service_framework.utils import logging_utils, service_utils, utils


def main():
    """
    ~~~ Main Entry to the Framework ~~~
    """
    args, unknown_args = get_arguments()

    logger_args_dict = {
        'console_loglevel': args.console_loglevel,
        'log_folder': args.log_folder,
        'file_loglevel': args.file_loglevel,
        'backup_count': args.backup_count,
    }

    log = logging_utils.setup_package_logger(
        None,
        **logger_args_dict
    )

    log.info('Starting service...')
    imported_service = utils.import_python_file_from_cwd(args.service_path)

    config = service_utils.setup_config(args.config_path, unknown_args, imported_service)
    addresses = service_utils.setup_addresses(args.addresses_path, imported_service, config)
    connections = service_utils.setup_connections(addresses, imported_service, config)
    states = service_utils.setup_states(addresses, imported_service, config)

    service_utils.setup_sigint_handler_func(
        imported_service,
        config,
        connections,
        states,
        logger_args_dict
    )

    if args.main_mode:
        service_utils.run_main(config, connections, states, imported_service.main, logger_args_dict)

    else:
        service_utils.run_service(config, connections, states, logger_args_dict)


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
