""" File to house a replyer service """

from service_framework import get_logger

LOG = get_logger()


def setup_config(config):
    """
    Setup ~~ all the things ~~
    """
    config['response_text'] = config.get('response_text', 'DEFAULT')
    return config


def on_new_request(args, to_send, config):
    """
    Method triggered when a new request is recieved from
    a requester.
    """
    LOG.info('Got payload: %s', args)
    response = {'echoed': f'{config["response_text"]} {args["to_echo"]}'}
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
                'to_echo': str,
            },
            'required_return_arguments': {
                'echoed': str,
            }
        }
    }
}
