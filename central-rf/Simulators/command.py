#!/usr/bin/python
import sys
import zmq

if __name__ == '__main__':
    # Check there is one string argument TODO
    if len(sys.argv) != 2:
        print("Exactly one argument is expected!")
        sys.exit(1)

    context = zmq.Context()
    command = context.socket(zmq.REQ)
    command.connect("ipc:///tmp/alarm-system/command.ipc")
    command.send(sys.argv[1])
    reply = command.recv()
    print("reply: " + reply)

