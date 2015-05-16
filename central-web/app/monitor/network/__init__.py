from time import time
from . import devices_manager

#TODO define standard Event types and structure
class EventType:
    STOP = 0
    LOCK_CODE = 1
    UNLOCK_CODE = 2
    PING = 3
    VOLTAGE = 4

class Event:
    def __init__(self, event_type, device_id = None, detail = None):
        self.timestamp = time()
        self.event_type = event_type
        self.device_id = device_id
        self.detail = detail
