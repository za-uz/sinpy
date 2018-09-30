"""
sinpy/essico/chck

Usage:
  chck [-f ENDPOINT] [-t ENDPOINT] [-p ENDPOINT]

Options:
  -f ENDPOINT   Endpoint from where to PULL transactions from.
                Default is ipc:///tmp/feeds/sin/recv/0
  -t ENDPOINT   Endpoint to PUSH transactions to.
                Default is ipc:///tmp/feeds/sin/send/0
  -p ENDPOINT   REP Endpoint of the prst component
                Default is ipc:///tmp/feeds/sin/prst/0

Examples:
  chck -t ipc:///tmp/feeds/sin/mnky/0
"""

from docopt import docopt
import zmq
from iotautils import timestamp_ok, curlhash, pow_done, Quatrits

def main():
    arguments = docopt(__doc__)

    if arguments['-f'] == None:
        arguments['-f'] = 'ipc:///tmp/feeds/sin/recv/0'
    if arguments['-t'] == None:
        arguments['-t'] = 'ipc:///tmp/feeds/sin/send/0'
    if arguments['-p'] == None:
        arguments['-p'] = 'ipc:///tmp/feeds/sin/prst/0'

    context = zmq.Context()

    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(arguments['-f'])

    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(arguments['-t'])

    req_socket = context.socket(zmq.REQ)
    req_socket.connect(arguments['-p'])

    try:
        while True:
            tx = Quatrits(8019, pull_socket.recv())
            
            print('Received a transaction.')
            
            if not timestamp_ok(tx):
                continue
            tx_hash = curlhash(tx)
            if not pow_done(tx_hash):
                continue
            
            req_socket.send(b'exist' + bytes(tx_hash))
            response = req_socket.recv()

            if response == b'y':
                continue

            req_socket.send(b'store' + bytes(tx))
            response = req_socket.recv()

            if response == b'n':
                continue

            print('srvvd all')
            push_socket.send(bytes(tx))


    except KeyboardInterrupt:
        print('\nShutting down...')
        pull_socket.close()
        push_socket.close()
        req_socket.close()
        context.destroy()


if __name__ == '__main__':
    main()
