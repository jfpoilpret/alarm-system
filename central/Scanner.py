#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from app.nrf24 import NRF24

NETWORK = 0xC05A
#TODO use command line options to specify device to simulate as listener
SERVER_ID = 0x01

CE_PIN = 25

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    hexa = lambda s: int(s, 16)
    parser.add_argument('--target', type = hexa, default = SERVER_ID)
    #parser.add_argument('--cipher')
    args = parser.parse_args()
    device = args.target & 0xFF
    print "Scanner on target device %02x..." % device
    nrf = NRF24(NETWORK, device)
    print "NRF24 instance created..."
    nrf.begin(0, 0, CE_PIN, False)
    print "NRF24 instance started..."
    while True:
        payload = nrf.recv(5)
        if payload:
            print "Source %02X, port %02X" % (payload.device, payload.port)
            content = payload.content
            if content:
                output = ''
                for c in content:
                    output += '%02x ' % c
                print output

