"""
sinpy/essico/recv

Usage:
  recv [-t ENDPOINT] [-f ENDPOINT]

Options:
  -f ENDPOINT   Local endpoint on which to listen for PUB connections.
                Default is "tcp://*:14637". I.e. Listen on tcp port 14637.
                More info here: http://api.zeromq.org/4-2:zmq-bind
  -t ENDPOINT   Local endpoint to PUSH transactions to.
                Default is ipc:///tmp/feeds/sin/recv/0

Examples:
  recv -f tcp://*:14637 -t ipc:///tmp/feeds/sin/recv/0
"""

from docopt import docopt
import zmq
import os

def main():
    arguments = docopt(__doc__)

    if arguments['-t'] == None:
        arguments['-t'] = "ipc:///tmp/feeds/sin/recv/0"
        if not os.path.exists('/tmp/feeds/sin/recv'):
            os.makedirs('/tmp/feeds/sin/recv')
    if arguments['-f'] == None:
        arguments['-f'] = "tcp://*:14637"
    
    context = zmq.Context()

    sub_socket = context.socket(zmq.SUB)
    sub_socket.bind(arguments['-f'])
    sub_socket.setsockopt(zmq.SUBSCRIBE, b'') # listen to all topics

    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(arguments['-t'])

    print("recv started.")

    try:
        while True:
            push_socket.send(sub_socket.recv())
    except KeyboardInterrupt:
        print('\nShutting down...')
        sub_socket.close()
        push_socket.close()
        context.destroy()

if __name__ == '__main__':
    main()
else:
    raise Error()
