""" Intermediary as an X-Pub X-Sub """

import argparse
import zmq


def main():
    """
    Intermediary for Publisher and Subscriber
    """
    parser = argparse.ArgumentParser(description='Intermediary service between pubs and subs.')
    parser.add_argument('-s', '--sub_port', default=27000, help='The port to connect publishers.')
    parser.add_argument('-p', '--pub_port', default=37000, help='the port to connect subscribers.')
    args = parser.parse_args()
    print('Running with namespace:', args)


    context = zmq.Context()

    # Socket for Publishers
    print('Listenening for Publishers on:', args.sub_port)
    backend = context.socket(zmq.XSUB)
    backend.bind('tcp://*:{}'.format(args.sub_port))

    # Socket for Subscribers
    print('Listenening for Subscribers on:', args.pub_port)
    frontend = context.socket(zmq.XPUB)
    frontend.bind('tcp://*:{}'.format(args.pub_port))

    print('Starting Pub Sub Intermediary Bus...')
    zmq.proxy(frontend, backend)

    # Clean up.. maybe
    #frontend.close()
    #backend.close()
    #context.term()


if __name__ == '__main__':
    main()
