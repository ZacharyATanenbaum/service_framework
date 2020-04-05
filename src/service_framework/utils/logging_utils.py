""" File for housing logging utilities """

import logging
from logging.handlers import TimedRotatingFileHandler
from service_framework.utils.constants import PACKAGE_LOGGER_NAME


class WorkflowIdFilter(logging.Filter):
    """
    This filter is used to inject workflow id into the logging stream
    when a workflow id is present...
    """
    def __init__(self, workflow_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workflow_id = workflow_id

    def filter(self, record):
        record.workflow_id = self.workflow_id
        return True

    def __repr__(self):
        super_repr = super().__repr__()
        return super_repr + ' FILTER: workflow_id'


def set_new_workflow_id_on_logger(workflow_id, logger_args_dict):
    """
    This is used to set the workflow id when a new message has arrived.
    Or, when done processing a new message that has arrived.
    workflow_id::str
    logger_args_dict = {
        console_loglevel: str,
        log_folder: None,
        file_loglevel: str,
        backup_count: int,
    }
    """
    logger = logging.getLogger(PACKAGE_LOGGER_NAME)
    logger.handlers = []
    setup_package_logger(workflow_id, **logger_args_dict)


def setup_package_logger(workflow_id=None,
                         console_loglevel='INFO',
                         log_path=None,
                         file_loglevel='INFO',
                         backup_count=24):
    """
    Pass
    """
    logger = logging.getLogger(PACKAGE_LOGGER_NAME)
    logger.setLevel('DEBUG')

    if logger.handlers:
        logger.debug('"%s" already setup - skipping logger...', PACKAGE_LOGGER_NAME)
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(workflow_id)s - %(levelname)s - %(message)s'
    )

    if console_loglevel:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_loglevel)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(WorkflowIdFilter(workflow_id, name='workflow_id'))
        logger.addHandler(console_handler)

    if log_path:
        file_handler = TimedRotatingFileHandler(
            log_path,
            when='h',
            backupCount=backup_count
        )
        file_handler.setLevel(file_loglevel)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(WorkflowIdFilter(workflow_id, name='workflow_id'))
        logger.addHandler(file_handler)

    return logger


def get_logger():
    """
    This function is used to get the service framework package level logger...
    """
    return logging.getLogger(PACKAGE_LOGGER_NAME)
