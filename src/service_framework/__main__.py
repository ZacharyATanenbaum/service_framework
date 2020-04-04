""" Main Function for the Service Framework """

import argparse
from .utils import config_utils, utils
from .service import Service


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
        log_path=args.log_path,
        file_loglevel=args.file_loglevel,
        backup_count=args.backup_count
    )

    if args.main_mode:
        service.run_service_as_main_blocking()
    else:
        service.run_service_blocking()


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
    parser.add_argument('-bc', '--backup_count', default=24, help='Num of hourly file backups')
    parser.add_argument('-f', '--file_loglevel', default='INFO', help='See name')
    parser.add_argument('-l', '--log_path', default=None, help='Log file path')

    args, unknown_args = parser.parse_known_args()
    print('Using Arguments:', args)
    print('Got unknown Arguments:', unknown_args)
    return args, unknown_args


if __name__ == '__main__':
    main()
