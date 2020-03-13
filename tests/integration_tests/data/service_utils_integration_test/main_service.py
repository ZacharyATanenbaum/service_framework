""" Basic service for testing the service_utils run_main """

def main(to_send, config):
    print('Hello World Main...')


connection_models = {
    'out': {
        'out_connection_1': {
            'connection_type': 'requester',
            'required_arguments': {
                'this_is_a_test_arg': str,
            },
            'required_return_arguments': {
                'this_is_a_return_arg': str,
            },
        }
    }
}
