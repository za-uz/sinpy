"""
sinpy/essico/send

Usage:
  send [-f ENDPOINT] -n ENDPOINTS

Options:
  -f ENDPOINT   Local Endpoint on which to bind to to get transactions. (PULL)
                Default is "ipc:///tmp/feeds/sin/send/0".
  -n ENDPOINTS  Endpoints (=neighbors), seperated by spaces, to PUBlish
                transactions to. Don't forget quotation marks.

Examples:
  send -f ipc:///tmp/feeds/sin/send/0 -n "tcp://10.0.0.10:14637 tcp://10.0.0.92:14637"
"""

from docopt import docopt
import os
import zmq

def main():
    arguments = docopt(__doc__)

    if arguments['-f'] == None:
        arguments['-f'] = "ipc:///tmp/feeds/sin/send/0"
        if not os.path.exists('/tmp/feeds/sin/send'):
            os.makedirs('/tmp/feeds/sin/send')

    context = zmq.Context()
    
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind(arguments['-f'])

    neighbor_sockets = []
    for n in arguments['-n'].split():
        s = context.socket(zmq.PUB)
        s.connect(n)
        neighbor_sockets.append(s)
    
    print("send started.")

    try:
        while True:
            packet = pull_socket.recv()
            for s in neighbor_sockets:
                s.send(packet)
    except KeyboardInterrupt:
        print('\nShutting down...')
        pull_socket.close()
        for s in neighbor_sockets:
            s.close()
        context.destroy()

if __name__ == '__main__':
    main()
else:
    raise Error()
