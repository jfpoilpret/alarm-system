# -*- coding: utf-8 -*-
import struct
import time

from threading import Thread
from ..cipher import XTEA
from queue import Queue
from app.monitor.monitoring import AlarmStatus
from app.monitor.network.events import Event, EventType
from app.monitor.network.message import MessageType

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
    
class PingHandler:
    def __init__(self, manager, key_refresh_period):
        self.key_gen = KeyGenerator()
        self.key_gen.start()
        self.manager = manager
        self.key_refresh_period = key_refresh_period
    
    def _status(self):
        return self.manager.status == AlarmStatus.LOCKED
    
    def __call__(self, nrf, device, port, content):
        id = device.source.device_id
        now = time.time()
        payload = [self._status()]
        # Check if need to generate and send new cipher key
        if now >= device.next_key_time:
            key = self.key_gen.get_key()
            payload += ppack('<4L', key[0], key[1], key[2], key[3])
            if nrf.send(id, port, payload) > 0:
                device.cipher.set_key(key)
                device.next_key_time = now + self.key_refresh_period
            print("Source %02x, port %02x" % (id, port))
            print('Generated new key, payload = %s' % payload)
        else:
            nrf.send(id, port, payload)
            print("Source %02x, port %02x" % (id, port))
        return Event(EventType.PING, id)
    
class VoltageHandler:
    def __init__(self):
        pass
    
    def __call__(self, nrf, device, port, content):
        id = device.source.device_id
        voltage = punpack('<H', content)[0]
        print("Source %02x, voltage = %d mV" % (id, voltage))
        return Event(EventType.VOLTAGE, id, voltage)
    
class LockUnlockHandler:
    def __init__(self, manager):
        self.manager = manager
    
    def _status(self):
        return self.manager.status == AlarmStatus.LOCKED
    
    def __call__(self, nrf, device, port, content):
        id = device.source.device_id
        code = punpack('<2L', content)
        code = device.cipher.decipher(code)
        code = struct.pack('2L', code[0], code[1])
        code = struct.pack('6s', code[0:6])
        # Send current lock status
        nrf.send(id, port, [self._status()])
        print("Source %02x, code = %s" % (id, code))
        #TODO return the event to push to the events queue
        event_type = EventType.LOCK_CODE if port == MessageType.LOCK_CODE else EventType.UNLOCK_CODE
        return Event(event_type, id, code)
    