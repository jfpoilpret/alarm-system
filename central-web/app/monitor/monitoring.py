# encoding: utf-8

from queue import Queue
from threading import Thread
from time import time

from app import db
from app.models import Alert, AlertType
from app.monitor.network import Event, EventType
from app.monitor.network.devices_manager import DevicesManager, DevicesManagerSimulator

class AlarmStatus:
    LOCKED = 1
    UNLOCKED = 2
    
class LiveDevice:
    def __init__(self, device):
        self.source = device
        self.latest_ping = 0
        self.latest_voltage_level = None

class MonitoringManager(Thread):
    def __init__(self, app):
        self.status = None
        if app.config['SIMULATE_DEVICES']:
            self.devices_manager_class = DevicesManagerSimulator
        else:
            self.devices_manager_class = DevicesManager
    
    def activate(self, config):
        self.status = AlarmStatus.LOCKED
        self.config_id = config.id
        # Store lock code from config
        self.lock_code = config.lock_code
        # Create dictionary of LiveDevices from config
        self.devices = {id: LiveDevice(device) for id, device in config.devices.items()}
        # Start thread that reads queues and act upon received messages (DB, SMS...)
        # Create the event queue that will be used by DevicesManager
        self.event_queue = Queue()
        self.start()
        # Instantiate DevicesManager (based on app.config)
        self.devices_manager = self.devices_manager_class(self.event_queue)
    
    def deactivate(self):
        # Stop DevicesManager
        self.devices_manager.deactivate()
        self.devices_manager = None
        # Then stop thread by sending special event to queue
        self.event_queue.put(Event(EventType.STOP))
        # Wait until thread is finished
        self.join()
        # Finally clear all configuration
        self.config_id = None
        self.lock_code = None
        self.status = None
        self.devices = {}
    
    #FIXME should we clone each device under locking (multi-thread!!!)
    def get_devices(self):
        return self.devices

    #TODO redesign to avoid if elif elif ... else
    def run(self):
        while True:
            event = self.event_queue.get()
            # Detect stop condition
            if event.event_type == EventType.STOP:
                return
            alert = None
            device = self.devices[event.device_id]
            device.latest_ping = event.timestamp
            # Check event type and decide what to do with it
            if event.event_type == EventType.VOLTAGE:
                device.latest_voltage_level = event.detail
                if device.latest_voltage_level < device.source.voltage_threshold:
                    message = 'Module %s current voltage (%fV) is under threshold (%fV)' % (
                        device.source.name, device.latest_voltage_level, device.source.voltage_threshold)
                    alert = Alert(
                        level = Alert.LEVEL_WARNING,
                        alert_type = AlertType.DEVICE_VOLTAGE_UNDER_THRESHOLD,
                        message = message)
            elif event.event_type in [EventType.LOCK_CODE, EventType.UNLOCK_CODE]:
                if self.lock_code != event.detail:
                    message = 'Bad code typed on module %s' % device.source.name
                    alert = Alert(
                        level = Alert.LEVEL_WARNING,
                        alert_type = AlertType.WRONG_LOCK_CODE,
                        message = message)
                else:
                    if event.event_type == EventType.LOCK_CODE:
                        self.status = AlarmStatus.LOCKED
                        alert_type = AlertType.LOCK
                    else:
                        self.status = AlarmStatus.UNLOCKED
                        alert_type = AlertType.UNLOCK
                    self.devices_manager.set_status(self.status)
                    alert = Alert(
                        level = Alert.LEVEL_INFO, 
                        alert_type = alert_type)
            if alert:
                alert.when = event.timestamp
                alert.config_id = self.config_id
                alert.device_id = device.source.device_id
                db.session.add(alert)
                db.session.commit()
                    