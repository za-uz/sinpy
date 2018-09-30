"""
sinpy/essico/mnky

Usage:
  mnky [-t ENDPOINT] [-f ENDPOINT]

Options:
  -f ENDPOINT   Local endpoint from which to PULL transactions from.
                Default is "ipc:///tmp/feeds/sin/mnky/in/0". I.e. Listen
                on tcp port 14637.
                More info here: http://api.zeromq.org/4-2:zmq-bind
  -t ENDPOINT   Local endpoint to PUSH transactions to.
                Default is ipc:///tmp/feeds/sin/mnky/out/0
                More info here: http://api.zeromq.org/4-2:zmq-connect

Examples:
  mnky -f ipc:///tmp/feeds/sin/prxy/0 -t tcp://10.0.0.10:14637
"""

from docopt import docopt
import zmq

def main():
    arguments = docopt(__doc__)

    if arguments['-f'] == None:
        arguments['-f'] = "ipc:///tmp/feeds/sin/mnky/in/0"
    if arguments['-t'] == None:
        arguments['-t'] = "ipc:///tmp/feeds/sin/mnky/out/0"

    context = zmq.Context()

    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind(arguments['-f'])

    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind(arguments['-t'])
    
    print("monkey in the middle started.")

    try:
        while True:
            pub_socket.send(pull_socket.recv())
    except KeyboardInterrupt:
        print('\nShutting down...')
        pull_socket.close()
        pub_socket.close()
        context.destroy()

if __name__ == '__main__':
    main()
else:
    raise Error()
