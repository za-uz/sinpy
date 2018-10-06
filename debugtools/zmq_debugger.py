"""
zmq_debugger - General Purpose ZeroMQ Debugger

Usage:
  gpdb -s TYPE -e ENDPOINT (-b|-c) (-i|-o) [-x] [-t TOPIC]

Options:
  -s TYPE       PUB, SUB, PUSH, ... (http://api.zeromq.org/4-2:zmq-socket)
  -e ENDPOINT   Endpoint on which to listen or send transactions to.
                "tcp://*:14637". Listen on tcp port 14637.
                More info here: http://api.zeromq.org/4-2:zmq-bind
                      and here: http://api.zeromq.org/4-2:zmq-connect
  -b            bind, not connect
  -c            connect, not bind
  -i            Read from stdin, send to socket.
  -o            Receive from socket, write to stdout.
  -x            If on, input/output text is not UTF-8 but hexadecimal.
  -t TOPIC      The topic to subscribe to. Will be ignored, if the sockettype
                is not "SUB". Default value is "" (all topics).

Examples:
  gpdb -s PUB -e tcp://localhost:14637 -c -i
  gpdb -s PULL -e ipc:///tmp/feeds/sin/chck -c -o
"""

from docopt import docopt
import zmq

def main():
    arguments = docopt(__doc__)

    context = zmq.Context()
    socket_type = None

    if arguments['-s'] in ['PUB', 'SUB', 'ROUTER', 'DEALER', 'PUSH', 'PULL', 'PAIR']:
        socket_type = getattr(zmq, arguments['-s'])
    else:
        raise ValueError("-s must be one of 'PUB', 'SUB', 'ROUTER', 'DEALER', 'PUSH', 'PULL', 'PAIR'")

    socket = context.socket(socket_type)

    if arguments['-b']:
        socket.bind(arguments['-e'])
    elif arguments['-c']:
        socket.connect(arguments['-e'])
    else:
        context.destroy()
        raise RuntimeError

    if socket_type == zmq.SUB:
        socket.setsockopt(zmq.SUBSCRIBE,
                          arguments['-t'].encode() if arguments['-t'] != None else b'')

    try:
        if arguments['-i']:
            while True:
                if arguments['-x']:
                    socket.send(bytes.fromhex(input('send-hex> ')))
                else:
                    socket.send(input('send-utf> ').encode())
        elif arguments['-o']:
            while True:
                if arguments['-x']:
                    print('recv-hex: ' + socket.recv().hex())
                else:
                    print('recv-utf: ' + socket.recv().decode())
    except KeyboardInterrupt:
        print('\nShutting down...')
        socket.close()
        context.destroy()

if __name__ == '__main__':
    main()
else:
    raise Error()
