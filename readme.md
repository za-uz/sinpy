# SINPY

> More information can be found in the [SIN Wiki](https://github.com/za-uz/sin/wiki).

SINPY stands  for the PYthon version of a "Scalable Iota Node". It is supposed
to be an Iota Full Node consisting of multiple Python scripts which can
communicate with each other via [ØMQ][1]. They can also communicate with
programs written in other languages to increase performance. These programs can
run on the same computer but they don't have to. They could also run on 10
Raspberry Pi Zeroes enabling an early form of Swarm nodes.

SINPY seperates all functions of an Iota Full Node into their own programs.
It does this for two reasons:
 * Code stays more readable and maintanable
   The code is indeed very understandable (for me) at the moment. But there
   are hardly any functions already implemented. Fingers crossed it will stay
   readable with the other functions. There are currently some "bad practices"
   in the code. I have to figure something out about how to remove them while
   still keeping the current simplicity. If you have any suggestions, I'd
   appreciate it, if you'd open an issue or made a pull request.
 * Scalability
   Because all features are seperate programs that communicate over ØMQ, they
   can be run on multiple computers.


## ESSICOs

Currently, there are 4 components implemented:
 * recv.py
   Receives transactions and forwards them to chck.
 * chck.py
   Checks basic properties of a transaction i.e. timestamp, PoW, duplicate
   If all properties are ok, it stores sends them to prst and send
 * prst.py
   Stores transactions. Currently in sqlite3 file. Could be replaced by
   scalable database.
 * send
   Forwards all transactions it gets to the "neighbors" (other SINPY nodes
   or IRI Nodes in the future).

I called these components "ESSential Iota COmponents".

They are connected to each other like this:

The REQ, REP, PUB, SUB, etc. represent ØMQ socket types. The components that
have a dot bind() the ones without a dot on their side connect().

![Architecture](https://svgshare.com/i/8by.svg)

Other components will/could include:
 * iri_recv.py
 * iri_send.py
 * Bundle Validation
 * Bundle Confirmation (Milestones, etc.)
 * Snapshots
 * Some kind of IXI-Module interpreter
 * REST-API
 * Pearldiver(s)

## How to "use"

SINPY can't even communicate with real Iota Full Nodes at this point in time
so it is kind of useless at the moment. But still: Here is how you can test it:

* get [docker (and docker-compose)][2]
* get [python][3]
* get pipenv (`pip install pipenv`)
* clone the sinpy repository (`git clone https://github.com/za-uz/sinpy.git`)
* navigate into the sinpy repository
* open the `docker-compose.yml` file in a text editor
  * on the last line `- myhost:172.17.0.1`, instead of 172.17.0.1 type your docker0 IP address
  * you can get your docker0 IP address with the following command:
    * on Linux and Mac OS: `ip addr show docker0`
    * on Windows:
  * close the `docker-compose.yml` file
* run `docker-compose up -d --build` in the sinpy directory
* start the genesissender
  * open a new terminal window in the sinpy directory
  * run `pipenv shell`
  * run `python debugtools/genesissender.py -e tcp://127.0.0.1:14637 -c`
* start the transaction receiver
  * open a new terminal window in the sinpy directory
  * run `pipenv shell`
  * run `python debugtools/zmq_debugger.py -s SUB -e tcp://*:14641 -b -o -x`

### Expected behaviour:

When you press `<Enter>` in the genesissender, the transaction should arrive at
the transaction receiver ~a second later. When you press `<Enter>` again, the
transaction should not appear at the transaction receiver because it was stopped
at the `chck` component because it was already in the database.

---

If you have any questions about anything, please to open an issue or talk to me
on the Iota Discord.

---

Originally I started to write the "SIN" in C. Because it is literally
impossible to use argument parsers in C (if it were possible, I would've been
able to do it) and because I am not yet very good in C (definitely unrelated to
the first problem) I decided to prototype the whole thing in Python. Since the
individual components communicate via ØMQ, it is possible to gradually implement
C versions of them.

[1]: http://zeromq.org/
[2]: https://www.docker.com/
[3]: https://www.python.org/
