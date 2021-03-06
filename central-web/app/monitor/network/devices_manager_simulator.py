# encoding: utf-8

from threading import Thread
from threading import Event as ThreadEvent
from random import Random
from app.monitor.events import EventType, Event
from app.models import Device
from app.monitor.network.common_devices_manager import AbstractDevicesManager

class DevicesManagerSimulator(AbstractDevicesManager, Thread):
    def __init__(self, *args, **kwargs):
        AbstractDevicesManager.__init__(self, *args, **kwargs)
        Thread.__init__(self)
        self.random = Random()
        self.stop = ThreadEvent()
        self.stop.clear()
        self.start()
        
    def deactivate(self):
        self.stop.set()
        self.join()
    
    def run(self):
        keypads = [device.source.device_id for device in self.devices.values() if device.source.kind == Device.KIND_KEYPAD]
        while True:
            self.stop.wait(10.0)
            if self.stop.is_set():
                return
            # Simulate Device events randomly
            device_id = self.random.choice(list(self.devices.keys()))
            event_type = self.random.choice([EventType.PING, EventType.VOLTAGE])
            voltage = self.random.uniform(2.3, 3.0)
            event = Event(event_type, device_id, voltage)
            self.queue.put(event)
            # Less often (5% of the time), we can trigger lock/unlock events
            if self.random.random() < 0.05:
                device_id = self.random.choice(keypads)
                event_type = self.random.choice([EventType.LOCK_CODE, EventType.UNLOCK_CODE])
                code = '%06s' % self.random.randint(0, 999999)
                event = Event(event_type, device_id, code)
                self.queue.put(event)
