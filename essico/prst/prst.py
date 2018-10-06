'''
sinpy/essico/prst

Usage:
  prst [-p ENDPOINT] [-d NAME]

Options:
  -p ENDPOINT   Local REP Endpoint of the prst component
                Default is ipc:///tmp/feeds/sin/prst/0
  -d NAME       Filename (and/or path) of the SQLite3 file
                DEfault is ./iota.db

Examples:
  prst -p tcp://10.0.0.10:12314
'''

from docopt import docopt
import zmq
import sqlite3
from iotautils import Quatrits
import time

QTX_HASH_SIZE = 61
QTX_SIZE = 2005

DB_TABLE = 'iota_transaction'
DB_HASH_COL = 'tx_hash'
DB_DATA_COL = 'quatrits'

GET_TX_STMT = "SELECT " + DB_DATA_COL + " FROM " + DB_TABLE + " WHERE " + DB_HASH_COL + " == ?;"           
PUT_TX_STMT = "INSERT INTO " + DB_TABLE + " VALUES (?, ?);"     
CREATE_TABLE_STMT = 'CREATE TABLE IF NOT EXISTS ' + DB_TABLE + ' (' + DB_HASH_COL + ' BLOB PRIMARY KEY, ' + DB_DATA_COL + ' BLOB);'

def main():
    arguments = docopt(__doc__)

    if arguments['-p'] == None:
        arguments['-p'] = 'ipc:///tmp/feeds/sin/prst/0'
    if arguments['-d'] == None:
        arguments['-d'] = './iota.db'

    context = zmq.Context()

    rep_socket = context.socket(zmq.REP)
    rep_socket.bind(arguments['-p'])

    db_conn = sqlite3.connect(arguments['-d'])
    cursor = db_conn.cursor()
    last_commit = time.time()
    cursor.execute(CREATE_TABLE_STMT)
    
    print('prst started.')

    try:
        while True:
            request = rep_socket.recv()
            if request.startswith(b'exist'):
                packet = request.split(b'exist', 1)[1]
                tx_hash = Quatrits(243, packet)
                cursor.execute(GET_TX_STMT, (bytes(tx_hash),))
                if cursor.fetchone() != None:
                    rep_socket.send(b'y') # yes, it exists
                else:
                    rep_socket.send(b'n') # no, it doesn't exist
            elif request.startswith(b'store'):
                rep_socket.send(b'y') # yes, I'm trying to store it
                packet = request.split(b'store', 1)[1]
                tx_hash = Quatrits(243, packet[0:QTX_HASH_SIZE])
                tx = Quatrits(8019, packet[QTX_HASH_SIZE:QTX_HASH_SIZE+QTX_SIZE])
                cursor.execute(PUT_TX_STMT, (bytes(tx_hash), bytes(tx)))
            else:
                rep_socket.send(b'e') # error

            if time.time() - last_commit >= 9: # commit every ~9 seconds
                last_commit = time.time()
                print("db commit at: %f" % last_commit)
                db_conn.commit()



    except KeyboardInterrupt:
        print('\nShutting down...')
        db_conn.commit()
        db_conn.close()
        rep_socket.close()
        context.destroy()

if __name__ == '__main__':
    main()

