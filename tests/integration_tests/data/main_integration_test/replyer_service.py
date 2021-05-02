""" File to house a replyer service """

from logging import getLogger

LOG = getLogger(__name__)


def on_new_request(args, to_send, config):
    """
    Method triggered when a new request is recieved from
    a requester.
    """
    LOG.info('Got payload: %s', args)
    response = {'echoed': args['to_echo']}
    LOG.info('Responding with: %s', response)
    return response


connection_models = {
    'in': {
        'reply': {
            'connection_type': 'replyer',
            'required_creation_arguments': {
                'connection_function': on_new_request,
            },
            'required_arguments': {
                'to_echo': str,
            },
            'required_return_arguments': {
                'echoed': str,
            }
        }
    }
}
