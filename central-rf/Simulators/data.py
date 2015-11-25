#!/usr/bin/python
import zmq

if __name__ == '__main__':
    context = zmq.Context()
    data = context.socket(zmq.SUB)
    data.connect("ipc:///tmp/alarm-system/devices.ipc")
    data.setsockopt(zmq.SUBSCRIBE, "")
    while True:
        msg = data.recv()
        if msg:
            print(msg)

