#!/usr/bin/python
# -*- coding: utf-8 -*-
import struct
import time

from threading import Thread
from app.nrf24 import NRF24
from app.cipher import XTEA
from app.message import MessageType
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
    def __init__(self, id):
        self.id = id
        self.cipher = XTEA()
        self.latest_ping = 0
        self.latest_voltage_level = None
        self.next_key_time = 0

class PingHandler:
    def __init__(self):
        self.key_gen = KeyGenerator()
        self.key_gen.start()
    
    def __call__(self, nrf, device, port, content):
        now = time.time()
        device.latest_ping = now
        payload = [self.locked]
        # Check if need to generate and send new cipher key
        if now >= device.next_key_time:
            key = self.key_gen.get_key()
            payload += ppack('<4L', key[0], key[1], key[2], key[3])
            if nrf.send(device.id, port, payload) > 0:
                device.cipher.set_key(key)
                device.next_key_time = now + MessageDispatcher.PERIOD_REFRESH_KEY_SECS
            print "Source %02x, port %02x" % (device.id, port)
            print 'Generated new key, payload = %s' % payload
        else:
            nrf.send(device.id, port, payload)
            print "Source %02x, port %02x" % (device.id, port)
    
class VoltageHandler:
    def __init__(self):
        pass
    
    def __call__(self, nrf, device, port, content):
        device.latest_voltage_level = punpack('<H', content)[0]
        print "Source %02x, voltage = %d mV" % (device.id, device.latest_voltage_level)
    
class LockUnlockHandler:
    def __init__(self):
        pass
    
    def __call__(self, nrf, device, port, content):
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
        nrf.send(device.id, port, [self.locked])
        print "Source %02x, code = %s" % (device.id, code)
    
class RF(NRF24):
    def send(self, device, port, payload):
        now = time.time()
        count = super(RF, self).send(device, port, payload)
        print "Send time = %.02f ms" % ((time.time() - now) * 1000.0)
        return count

#TODO improve design make settable handlers (callable classes or functions)
# def handle(device, port, content)
# TODO add queues for message handlers
class MessageDispatcher(Thread):
    # RF Communication constants
    NETWORK = 0xC05A
    SERVER_ID = 0x01
    # Hardware constants
    CE_PIN = 25
    # Timing constants
    PERIOD_REFRESH_KEY_SECS = 120.0
    
    def __init__(self, code, locked, devices = [], handlers = {}):
        self.nrf = RF(MessageDispatcher.NETWORK, MessageDispatcher.SERVER_ID)
        self.code = code
        self.locked = locked
        self.devices = {}
        for device in devices:
            self.devices[device] = Device(device)
        self.handlers = handlers
    
    def set_code(self, code):
        self.code = code
        
    def get_device(self, id):
        return self.devices[id]
        
    def run(self):
        self.nrf.begin(0, 0, MessageDispatcher.CE_PIN)
        while True:
            # Print some RF status
            print 'NRF24 trans = %d, retrans = %d, drops = %d' % (
                self.nrf.get_trans(), self.nrf.get_retrans(), self.nrf.get_drops())
            # Wait for remote modules calls
            payload = self.nrf.recv()
            if payload:
                now = time.time()
                self.handle_message(payload)
                print "Total time = %.02f ms" % ((time.time() - now) * 1000.0)
    
    def handle_message(self, payload):
        device = self.devices[payload.device]
        port = payload.port
        handler = self.handlers.get(port)
        if handler:
            handler(self.nrf, device, port, payload.content)
        else:
            print "Source %02x, unknown port %02x!" % (device.id, port)

