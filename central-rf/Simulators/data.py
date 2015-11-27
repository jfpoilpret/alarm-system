#!/usr/bin/python
import zmq

if __name__ == '__main__':
    context = zmq.Context()
    data = context.socket(zmq.SUB)
    data.connect("ipc:///tmp/alarm-system/devices.ipc")
    #data.setsockopt(zmq.SUBSCRIBE, "")
    data.setsockopt_string(zmq.SUBSCRIBE, "")
    while True:
        #msg = data.recv()
        msg = data.recv_string()
        if msg:
            print(msg)

