""" File to house the inline services class """

from service_framework.utils import service_utils


class InlineServices:
    """
    This class encompasses the framework to properly inline services.
    Instead of running services across multiple threads or processes
    this class will run them inline on one thread. Cutting out the
    connectivity behavior and greatly increasing the efficiency of
    the code
    """

    def __init__(self,
                 console_loglevel='INFO',
                 log_path=None,
                 file_loglevel='INFO',
                 backup_count=24,
                 service_loop_min_wait_time_s=0):
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

    def add_service(self, service_name, service_path, connections):
        pass

    def set_main_service(self, service_name, service_path):
        pass

    def set_main_service_by_module(self, service_name, service_module):
        pass
