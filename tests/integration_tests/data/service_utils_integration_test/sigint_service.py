""" File to house a requester service """

from service_framework.utils.logging_utils import get_logger
from service_framework.utils.utils import add_sigint_handler

LOG = get_logger()


def main(to_send, config):
    def sigint_handler_1(*_):
        LOG.info('SIGINT HANDLER 1 PROPERLY CALLED!!!')
        to_send('connection', 'sigint_output', {'message': 'handler1'})
        LOG.info('SENT SIGINT MESSAGE FROM HANDLER 1')

    add_sigint_handler(sigint_handler_1)

    while True:
        # Just keep waiting until it gets killed...
        pass


def sigint_handler(sigint, frame, to_send, states, config):
    LOG.info('SIGINT HANDLER 2 PROPERLY CALLED!!!')
    to_send('connection', 'sigint_output', {'message': 'handler2'})
    LOG.info('SENT SIGINT MESSAGE FROM HANDLER 2')


connection_models = {
    'out': {
        'sigint_output': {
            'connection_type': 'publisher',
            'required_arguments': {
                'message': str
            }
        }
    }
}
