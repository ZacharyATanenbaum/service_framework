""" Basic service for testing the service_utils """

def setup_addresses(addresses, config):
    """
    This method is called so addresses may be modified after addresses
    are populated from the provided addresses file and before the
    connections/states are created.
    """
    addresses['connections']['in']['in_connection_1']['in_conn_socket_3'] = 'test?'
    return addresses


def setup_config(config):
    """
    This method is called so the config may be modified after
    it has been populated from the config file + env variables but
    before the connections/states are created.
    """
    config['optional_1'] = 'optional_value_1'
    return config


config_model = {
    'required': {
        'config_1': str,
        'env_variable_1': str,
    },
    'optional': {
        'config_2': str,
        'env_variable_2': str,
        'optional_1': str,
    },
}
