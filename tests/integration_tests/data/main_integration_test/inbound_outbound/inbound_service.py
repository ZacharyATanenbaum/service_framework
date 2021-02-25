""" File to house a replyer service """

from service_framework import get_logger

LOG = get_logger()
QUEUE = []


def main(to_send, config):
    """
    Main method to do nothing while the "on_new_request"
    does all the work.
    """
    while True:
        if QUEUE:
            LOG.info('THING FROM QUEUE: %s', QUEUE.pop(0))
            LOG.info('SUCCESS!')


def on_new_request(args, to_send, config):
    """
    Method triggered when a new request is recieved from
    a requester.
    """
    LOG.info('Got payload: %s', args)
    converted = int(args['convert_this'])
    QUEUE.append(converted)
    response = {'converted': converted}
    LOG.info('Responding with: %s', response)
    return response


connection_models = {
    'in': {
        'reply': {
            'connection_type': 'replyer',
            'required_creation_arguments': {
                'on_new_request': on_new_request,
            },
            'required_arguments': {
                'convert_this': str,
            },
            'required_return_arguments': {
                'converted': int,
            }
        }
    }
}
