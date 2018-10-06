"""
dbugco/genesissender 
Sends (PUB) 2005 bytes (8019 Quatrits), all zeroed, to the endpoint.
This transaction has the following properties:
 * timestamp is always before the current time (zero)
 * PoW is done (curl(0) = 0)

Usage:
  genesissender [-e ENDPOINT] (-b|-c)

Options:
  -e ENDPOINT   Endpoint on which to PUBlish the transactions.
                Default is "tcp://localhost:14637".
                More info here: http://api.zeromq.org/4-2:zmq-bind
                      and here: http://api.zeromq.org/4-2:zmq-connect
  -b            bind, not connect
  -c            connect, not bind
"""


from docopt import docopt
import zmq

def main():
    arguments = docopt(__doc__)

    context = zmq.Context()

    socket = context.socket(zmq.PUB)

    if arguments['-e'] == None:
        arguments['-e'] = "tcp://localhost:14637"

    if arguments['-b']:
        socket.bind(arguments['-e'])
    else:
        socket.connect(arguments['-e'])

    try:
        while True:
            input('Press <Enter> jo send another Genesis transaction')
            socket.send(bytes(2005))
    except KeyboardInterrupt:
        print('\nShutting down...')
        socket.close()
        context.destroy()

if __name__ == '__main__':
    main()
else:
    raise Error()
