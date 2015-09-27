# encoding: utf-8

from time import time

#TODO define standard Event types and structure, add factory methods to create events of each type
class EventType(object):
    STOP = 0
    LOCK_CODE = 1
    UNLOCK_CODE = 2
    PING = 3
    VOLTAGE = 4
    NO_PING_FOR_LONG = 5
    
    TYPES_COUNT = NO_PING_FOR_LONG

class Event(object):
    def __init__(self, event_type, device_id = None, detail = None):
        self.timestamp = time()
        self.event_type = event_type
        self.device_id = device_id
        self.detail = detail
