# -*- coding: utf-8 -*-
from app.monitor.events import Event, EventType

class PingHandler:
    def __call__(self, verb, ts, id, device, args):
        return Event(EventType.PING, id, timestamp = ts)
    
class VoltageHandler:
    def __call__(self, verb, ts, id, device, args):
        voltage = int(args[0])
        print("Source %02x, voltage = %d mV" % (id, voltage))
        return Event(EventType.VOLTAGE, id, voltage, timestamp = ts)
    
class LockUnlockHandler:
    def __call__(self, verb, ts, id, device, args):
        code = args[0]
        # Send current lock status
        print("Source %02x, code = %s" % (id, code))
        event_type = EventType.LOCK_CODE if verb == 'LOCK' else EventType.UNLOCK_CODE
        return Event(event_type, id, code, timestamp = ts)
    
