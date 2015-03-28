#!/usr/bin/python
# -*- coding: utf-8 -*-
import struct
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

# Utility functions to pack/unpack payload
def ppack(format, *args):
    return [ord(x) for x in struct.pack(format, *args)]

def punpack(format, input):
    return struct.unpack(format, ''.join([chr(x) for x in input]))

class Device:
    def __init__(self):
        self.cipher = XTEA()
        self.latest_ping = time.time()
        self.latest_voltage_level = None
        self.next_key_time = 0
    
# List of all devices and their encoding keys
keys = {}

# Current alarm status
locked = 1

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
            #content = bytearray(payload.content)

            # Add the device if first time
            device = keys.get(device_id)
            if not device:
                device = Device()
                keys[device_id] = device
            print "Source %02x, port %02x" % (device_id, port)

            # Manage received message based on its type (port)
            if port == MessageType.PING_SERVER:
                device.latest_ping = now
                payload = [locked]
                # Check if need to generate and send new cipher key
                if now >= device.next_key_time:
                    key = XTEA.generate_key()
                    device.cipher.set_key(key)
                    device.next_key_time = now + PERIOD_REFRESH_KEY_SECS
                    payload += ppack('<4L', key[0], key[1], key[2], key[3])
                    print 'Generated new key, payload = %s' % payload
                nrf.send(device_id, port, payload)
            elif port == MessageType.VOLTAGE_LEVEL:
                device.latest_voltage_level = punpack('<H', content)[0]
                print "Source %02x, voltage = %d mV" % (device_id, device.latest_voltage_level)
            elif port in [MessageType.LOCK_CODE, MessageType.UNLOCK_CODE]:
                code = punpack('<2L', content)
                code = device.cipher.decipher(code)
                code = struct.pack('2L', code[0], code[1])
                code = struct.pack('6s', code[0:6])
                print "Source %02x, code = %s" % (device_id, code)
                # compare to CODE and update locked if needed
                if CODE == code:
                    if port == MessageType.LOCK_CODE:
                        locked = 1
                    else:
                        locked = 0
                # Send current lock status
                nrf.send(device_id, port, [locked])
            else:
                print "Source %02x, unknown port %02x!" % (device_id, port)

