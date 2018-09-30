"""
dbugco/rqrp - REQ-REP Socket debugger

Usage:
  rqrp -s TYPE -e ENDPOINT (-b|-c) [-x] 

Options:
  -s TYPE       REQ or REP socket type
  -e ENDPOINT   Endpoint on which to listen or send transactions to.
                "tcp://*:14637". Listen on tcp port 14637.
                More info here: http://api.zeromq.org/4-2:zmq-bind
                      and here: http://api.zeromq.org/4-2:zmq-connect
  -b            bind, not connect
  -c            connect, not bind
  -x            If on, input/output text is not UTF-8 but hexadecimal.
"""


from docopt import docopt
import zmq

def main():
    arguments = docopt(__doc__)

    context = zmq.Context()
    socket_type = None

    if arguments['-s'] == 'REQ':
        socket_type = zmq.REQ
    elif arguments['-s'] == 'REP':
        socket_type = zmq.REP
    else:
        raise ValueError("-s must be one of 'REQ', 'REP'")

    socket = context.socket(socket_type)

    if arguments['-b']:
        socket.bind(arguments['-e'])
    elif arguments['-c']:
        socket.connect(arguments['-e'])
    else:
        socket.close()
        context.destroy()
        raise RuntimeError

    try:
        while True:
            if arguments['-x'] and socket_type == zmq.REQ:
                socket.send(bytes.fromhex(input('req-hex> ')))
                print('rep-hex: ' + socket.recv().hex())
            elif socket_type == zmq.REQ:
                socket.send(input('req-utf> ').encode())
                print('rep-utf: ' + socket.recv().decode())
            elif arguments['-x']:
                print('req-hex: ' + socket.recv().hex())
                socket.send(bytes.fromhex(input('rep-hex> ')))
            else:
                    print('req-utf: ' + socket.recv().decode())
                    socket.send(input('rep-utf> ').encode())
    except KeyboardInterrupt:
        print('\nShutting down...')
        socket.close()
        context.destroy()

if __name__ == '__main__':
    main()
else:
    raise Error()
