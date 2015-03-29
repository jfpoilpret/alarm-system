#!/usr/bin/python
# -*- coding: utf-8 -*-
import struct
import time

from threading import Thread
from app.nrf24 import NRF24
from app.cipher import XTEA
from app.message import MessageType
import code
from Queue import Queue

# Utility functions to pack/unpack payload
def ppack(format, *args):
    return [ord(x) for x in struct.pack(format, *args)]

def punpack(format, input):
    return struct.unpack(format, ''.join([chr(x) for x in input]))

class KeyGenerator(Thread):
    QUEUE_SIZE = 64
    
    def __init__(self):
        self.queue = Queue(KeyGenerator.QUEUE_SIZE)
        pass
    
    def get_key(self):
        return self.queue.get()
    
    def run(self):
        while True:
            key = XTEA.generate_key()
            self.queue.put(key)
    
class Device:
    def __init__(self):
        self.cipher = XTEA()
        self.latest_ping = 0
        self.latest_voltage_level = None
        self.next_key_time = 0
    
class MessageHandler(Thread):
    # RF Communication constants
    NETWORK = 0xC05A
    SERVER_ID = 0x01
    # Hardware constants
    CE_PIN = 25
    # Timing constants
    PERIOD_REFRESH_KEY_SECS = 120.0
    
    def __init__(self, code, locked, devices):
        self.key_gen = KeyGenerator()
        self.key_gen.start()
        self.nrf = NRF24(MessageHandler.NETWORK, MessageHandler.SERVER_ID)
        self.code = code
        self.locked = locked
        self.devices = {}
        for device in devices:
            self.devices[device] = Device()
    
    def set_code(self, code):
        self.code = code
        
    def get_device(self, id):
        return self.devices[id]
        
    def run(self):
        self.nrf.begin(0, 0, MessageHandler.CE_PIN)
        while True:
            # Print some RF status
            print 'NRF24 trans = %d, retrans = %d, drops = %d' % (
                self.nrf.get_trans(), self.nrf.get_retrans(), self.nrf.get_drops())
            # Wait for remote modules calls
            # we limit timeout in order to frequently check that all known devices
            # are pinging as expected...
            payload = self.nrf.recv(10.0)
            if payload:
                now = time.time()
                self.handle_message(payload)
                print "Total time = %.02f ms" % ((time.time() - now) * 1000.0)
    
    def handle_message(self, payload):
        now = time.time()
        device_id = payload.device
        device = self.devices[device_id]
        port = payload.port
        content = payload.content

        # Manage received message based on its type (port)
        if port == MessageType.PING_SERVER:
            device.latest_ping = now
            payload = [self.locked]
            # Check if need to generate and send new cipher key
            if now >= device.next_key_time:
                key = self.key_gen.get_key()
                payload += ppack('<4L', key[0], key[1], key[2], key[3])
                if self.send(device_id, port, payload) > 0:
                    device.cipher.set_key(key)
                    device.next_key_time = now + MessageHandler.PERIOD_REFRESH_KEY_SECS
                print "Source %02x, port %02x" % (device_id, port)
                print 'Generated new key, payload = %s' % payload
            else:
                self.send(device_id, port, payload)
                print "Source %02x, port %02x" % (device_id, port)
        elif port == MessageType.VOLTAGE_LEVEL:
            device.latest_voltage_level = punpack('<H', content)[0]
            print "Source %02x, voltage = %d mV" % (device_id, device.latest_voltage_level)
        elif port in [MessageType.LOCK_CODE, MessageType.UNLOCK_CODE]:
            code = punpack('<2L', content)
            code = device.cipher.decipher(code)
            code = struct.pack('2L', code[0], code[1])
            code = struct.pack('6s', code[0:6])
            # compare to CODE and update locked if needed
            if self.code == code:
                if port == MessageType.LOCK_CODE:
                    self.locked = 1
                else:
                    self.locked = 0
            # Send current lock status
            self.send(device_id, port, [self.locked])
            print "Source %02x, code = %s" % (device_id, code)
        else:
            print "Source %02x, unknown port %02x!" % (device_id, port)
    
    def send(self, device, port, payload):
        now = time.time()
        count = self.nrf.send(device, port, payload)
        print "Send time = %.02f ms" % ((time.time() - now) * 1000.0)
        return count
