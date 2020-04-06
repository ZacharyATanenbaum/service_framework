""" File to house socket creation functions """

import time
import zmq

from service_framework.utils.logging_utils import get_logger
from service_framework.utils.msgpack_utils import msg_pack

LOG = get_logger()


def get_poller_socket(sockets_to_poll):
    """
    sockets_to_poll::[zmq.Context.Socket]
    return::zmq.Poller
    """
    poller = zmq.Poller()

    for socket in sockets_to_poll:
        poller.register(socket, zmq.POLLIN)

    return poller


def get_publisher_socket(address, context, is_x_pub=False, wait_after_creation_s=0.15):
    """
    address::str ex. "127.0.0.1:5001"
    context::zmq.Context()
    to_wait::float Time to wait prior to allowing "sending" on
                   this socket. Used to prevent the slow joiner
                   problem.
    """
    socket = context.socket(zmq.PUB)

    if is_x_pub:
        uri = 'tcp://%s' % address
        socket.connect(uri)
    else:
        port = address.split(':')[-1]
        uri = 'tcp://*:%s' % port
        socket.bind(uri)

    time.sleep(wait_after_creation_s)
    return socket


def get_requester_socket(address, context):
    """
    address::str ex. "127.0.0.1:5001"
    context::zmq.Context()
    """
    socket = context.socket(zmq.REQ)
    uri = 'tcp://%s' % address
    socket.connect(uri)
    return socket


def get_replyer_socket(address, context):
    """
    address::str ex. "127.0.0.1:5001"
    context::zmq.Context()
    """
    socket = context.socket(zmq.REP)
    port = address.split(':')[-1]
    uri = 'tcp://*:%s' % port
    socket.bind(uri)
    return socket


def get_subscriber_socket(address, context, tag=''):
    """
    address::str ex. "127.0.0.1:5001"
    context::zmq.Context()
    tag::str Tag to filter the subscriber by...
    is_x_sub::bool A flag to determine if XSUB or SUB should be used.
    """
    LOG.debug('Creating subscriber socket for address %s', address)
    socket = context.socket(zmq.SUB)
    uri = 'tcp://%s' % address

    if tag:
        socket.setsockopt(zmq.SUBSCRIBE, msg_pack(tag))
    else:
        socket.setsockopt_string(zmq.SUBSCRIBE, '')

    socket.connect(uri)
    return socket
