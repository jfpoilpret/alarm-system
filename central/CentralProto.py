#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from app.nrf24 import NRF24
from app.cipher import XTEA
from app.message import MessageType

# RF Communication constants
NETWORK = 0xC05A
SERVER_ID = 0x01

# Hardware constants
CE_PIN = 25

# Timing constants
PERIOD_REFRESH_KEY_SECS = 120.0

CODE = '123456'

#TODO refactor all conversion methods into a common place
def byte(val):
    return val & 0xFF

def to_int(val):
    return (byte(val[0]) << 8) + byte(val[1])

def to_long(val):
    return (byte(val[0]) << 24) + (byte(val[1]) << 16) + (byte(val[2]) << 8) + byte(val[3])

def from_long(val):
    return [byte(val >> 24), byte(val >> 16), byte(val >> 8), byte (val)]
    
def convert_key(key):
    key2 = []
    for i in key:
        key2 += from_long(i)
    return key2

class Device:
    def __init__(self):
        self.cipher = XTEA()
        self.latest_ping = time.time()
        self.latest_voltage_level = None
        self.next_key_time = 0
    
# List of all devices and their encoding keys
keys = {}

# Current alarm status
locked = True

if __name__ == '__main__':
    print "Alarm System Central Prototype..."
    nrf = NRF24(NETWORK, SERVER_ID)
    print "NRF24 instance created..."
    nrf.begin(0, 0, CE_PIN)
    print "NRF24 instance started..."
    while True:
        # Wait forever for remote modules calls
        #FIXME we should limit the timeout in order to frequently check that all known devices
        # are pinging as expected...
        payload = nrf.recv()
        now = time.clock()
        # Have we received something?
        if payload:
            # Yes, find the originating device and port (message type)
            device_id = payload.device
            port = payload.port
            content = payload.content

            # Add the device if first time
            device = keys.get(device_id)
            if not device:
                device = Device()
                keys[device_id] = device
            print "Source %02X, port %02X" % (device, port)

            # Manage received message based on its type (port)
            if port == MessageType.PING_SERVER:
                device.latest_ping = now
                payload = [locked]
                # Check if need to generate and send new cipher key
                if now >= device.next_key_time:
                    key = XTEA.generate_key()
                    device.cipher.set_key(key)
                    device.next_key_time = now + PERIOD_REFRESH_KEY_SECS
                    payload = [locked]
                    payload += convert_key(key)
                nrf.send(device_id, port, payload)
            elif port == MessageType.VOLTAGE_LEVEL:
                device.latest_voltage_level = to_int(content)
                print "Source %02X, voltage = %d mV" % (device, device.latest_voltage_level)
            elif port in [MessageType.LOCK_CODE, MessageType.UNLOCK_CODE]:
                #TODO decipher
                code = device.cipher.decipher([to_long(content[0:4]), to_long(content[4:8])])
                code = from_long(code[0]) + from_long(code[1])
                print "Source %02X, code = %s" % (device, code)
                #TODO convert to string and compare to CODE
                # Send current lock status
                nrf.send(device_id, port, [locked])
            else:
                print "Source %02X, unknown port %02X!" % (device, port)

