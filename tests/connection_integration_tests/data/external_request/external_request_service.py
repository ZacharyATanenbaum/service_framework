""" File to house a requester service """

import cbpro
from service_framework.utils.logging_utils import get_logger

LOG = get_logger()


def setup_connection_models(connections, config):
    """
    Properly setup connections before service is setup.
    """
    public_client = cbpro.PublicClient()

    def to_call(product_id):
        return public_client.get_product_ticker(product_id)

    connections['out']['external_request']['required_creation_arguments']['func_to_call'] = to_call
    return connections


def main(to_send, config):
    """
    This function is the main entrance into the Requester Service
    """
    product_id = config['product_id']

    LOG.info('Sending message out to Coinbase Pro for product_id: "%s"', product_id)
    response = to_send('external_request', {'product_id': product_id})
    LOG.info('Got response: %s', response)

    LOG.info('SUCCESS_HITTING_EXTERNAL_SERVICE')


config_model = {
    'required': {
        'product_id': str
    }
}

connection_models = {
    'out': {
        'external_request': {
            'connection_type': 'external_request',
            'required_creation_arguments': {
                'func_to_call': None,
            },
            'required_arguments': {
                'product_id': str
            },
            'required_return_arguments': {
                'trade_id': int,
                'price': str,
                'size': str,
                'bid': str,
                'ask': str,
                'volume': str,
                'time': str
            }
        }
    }
}
