#!/usr/bin/python
# -*- coding: utf-8 -*-
#from app.nrf24.nrf24 import NRF24
from app.nrf24 import NRF24

NETWORK = 0xC05A
#TODO use command line options to specify device to simulate as listener
SERVER_ID = 0x01

CE_PIN = 25

if __name__ == '__main__':
    print "Scanner..."
    nrf = NRF24(NETWORK, SERVER_ID)
    print "NRF24 instance created..."
    nrf.begin(0, 0, CE_PIN, False)
    print "NRF24 instance started..."
    #nrf.printDetails()
    while True:
        payload = nrf.recv(5)
        if payload:
            print "Source %02X, port %02X" % (payload.device, payload.port)
            content = payload.content
            output = ''
            for c in content:
                output += '%02x ' % c
            print output
