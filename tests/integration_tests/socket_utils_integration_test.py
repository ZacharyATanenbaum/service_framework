""" File to test socket utils """

import time
import zmq
from service_framework.utils import socket_utils

CONTEXT = zmq.Context()
REPLYER_ADDRESS = '127.0.0.1:9988'
REQUESTER_ADDRESS = '127.0.0.1:9988'


def test_socket_utils__get_requester_socket__get_replyer_socket__is_valid():
    """
    Make sure the function provides a proper requester socket...
    """
    test_string = 'This is a test string'
    requester = socket_utils.get_requester_socket(REQUESTER_ADDRESS, CONTEXT)
    replyer = socket_utils.get_replyer_socket(REPLYER_ADDRESS, CONTEXT)

    requester.send_string(test_string)
    request = replyer.recv_string()
    assert request == test_string


def test_socket_utils__get_poller_socket__proper_poller_provided():
    """
    Make sure that if x sockets are provided the poller will be
    properly created with all of the x sockets registered
    """
    requester = socket_utils.get_requester_socket(REQUESTER_ADDRESS, CONTEXT)
    replyer = socket_utils.get_replyer_socket(REPLYER_ADDRESS, CONTEXT)
    poller = socket_utils.get_poller_socket([replyer])

    test_string = 'This is also a test string'
    requester.send_string(test_string)

    start_time = time.time()
    while True:
        polled_socket = dict(poller.poll(0))

        if polled_socket:
            break

        if not polled_socket and time.time() - start_time > 0.2:
            break

    assert replyer in polled_socket
    assert polled_socket[replyer] == zmq.POLLIN
