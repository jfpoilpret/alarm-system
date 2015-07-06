# encoding: utf-8

from queue import Queue
from threading import Thread
from threading import Event as ThreadEvent
from datetime import datetime

from app import db
from app.models import Alert, AlertType
from app.monitor.network.events import Event, EventType
from app.monitor.network.devices_manager import DevicesManager, DevicesManagerSimulator
from time import sleep, time

monitoring_manager = None

class AlarmStatus(object):
    LOCKED = 1
    UNLOCKED = 2
    
class LiveDevice(object):
    def __init__(self, device):
        self.source = device.detached()
        self.latest_ping = 0
        self.latest_ping_alert_threshold = -1
        self.latest_voltage_level = None

class MonitoringManager(object):
    instance = None
    
    @staticmethod
    def create(app):
        MonitoringManager.instance = MonitoringManager(app)
        return MonitoringManager.instance
    
    def __init__(self, app):
        self.handlers = {
            EventType.VOLTAGE: self.handle_voltage_event,
            EventType.LOCK_CODE: self.handle_lock_event,
            EventType.UNLOCK_CODE: self.handle_unlock_event,
            EventType.NO_PING_FOR_LONG: self.handle_no_ping_for_long
        }
        self.app = app
        self.status = None
        self.active = False
        self.config_id = None
        self.lock_code = None
        self.devices = {}
        self.event_checker = None
        self.ping_checker_stop = ThreadEvent()
        self.ping_checker = None
        if app.config['SIMULATE_DEVICES']:
            self.devices_manager_class = DevicesManagerSimulator
        else:
            self.devices_manager_class = DevicesManager
    
    def activate(self, config):
        print('activate(%s)' % config.name)
        # Deactivate if already active
        self.deactivate()
        self.status = AlarmStatus.UNLOCKED
        self.config_id = config.id
        # Store lock code from config
        self.lock_code = config.lockcode
        #TODO Get the following values from config
        self.no_ping_time_thresholds = [
            (6.0, Alert.LEVEL_INFO), 
            (10.0, Alert.LEVEL_INFO), 
            (30.0, Alert.LEVEL_WARNING), 
            (60.0, Alert.LEVEL_WARNING), 
            (120.0, Alert.LEVEL_ALARM), 
            (300.0, Alert.LEVEL_ALARM), 
            (600.0, Alert.LEVEL_ALARM), 
            (3600.0, Alert.LEVEL_ALARM)]
        # Create dictionary of LiveDevices from config
        self.devices = {id: LiveDevice(device) for id, device in config.devices.items()}
        # Start thread that reads queues and act upon received messages (DB, SMS...)
        # Create the event queue that will be used by DevicesManager
        self.event_queue = Queue()
        self.event_checker = Thread(target = self.check_events)
        self.event_checker.start()
        self.active = True
        # Start check_pings thread
        self.ping_checker_stop.clear()
        self.ping_checker = Thread(target = self.check_pings)
        self.ping_checker.start()

        # Instantiate DevicesManager (based on app.config)
        self.devices_manager = self.devices_manager_class(self.event_queue, self.devices)
        
        # Create info alert
        self.store_alert(Alert(
            config_id = self.config_id,
            when = datetime.fromtimestamp(time()),
            level = Alert.LEVEL_INFO,
            alert_type = AlertType.SYSTEM_ACTIVATION,
            message = 'System activated',
            device = None))
        print('activate() thread started')
    
    def deactivate(self):
        print('deactivate()')
        if self.event_checker:
            # Stop DevicesManager
            self.devices_manager.deactivate()
            self.devices_manager = None
            # Then stop thread by sending special event to queue
            self.event_queue.put(Event(EventType.STOP))
            # Wait until thread is finished
            self.event_checker.join()
            self.event_checker = None
            # Wait for check_pings() thread to stop
            self.active = False
            self.ping_checker_stop.set()
            self.ping_checker.join()
            self.ping_checker = None
            # Finally clear all configuration
            config_id = self.config_id
            self.config_id = None
            self.lock_code = None
            self.status = None
            self.devices = {}
            # Create info alert
            self.store_alert(Alert(
                config_id = config_id,
                when = datetime.fromtimestamp(time()),
                level = Alert.LEVEL_INFO,
                alert_type = AlertType.SYSTEM_DEACTIVATION,
                message = 'System deactivated',
                device = None))
            print('deactivate() thread stopped')
    
    def lock(self):
        alert = self.create_lock_event(
            AlarmStatus.LOCKED, AlertType.LOCK, 'Lock through monitoring application')
        alert.when = datetime.fromtimestamp(time())
        alert.config_id = self.config_id
        self.store_alert(alert)
    
    def unlock(self):
        alert = self.create_lock_event(
            AlarmStatus.UNLOCKED, AlertType.UNLOCK, 'Unlock through monitoring application')
        alert.when = datetime.fromtimestamp(time())
        alert.config_id = self.config_id
        self.store_alert(alert)
    
    def get_status(self):
        return self.status
    
    #FIXME should we clone each device under locking (multi-thread!!!)
    def get_devices(self):
        return self.devices

    def store_alert(self, alert):
        with self.app.app_context():
            db.session.add(alert)
            db.session.commit()
    
    def check_pings(self):
        while not self.ping_checker_stop.is_set():
            # Perform check every 1 second
            self.ping_checker_stop.wait(1.0)
            if not self.active:
                return
            # Check list of all devices where last ping > 6 seconds
            time_limit = time() - self.no_ping_time_thresholds[0][0]
            #FIXME how to deal with devices that have not been connected yet (time = 0)?
            for id, dev in self.devices.items():
                if dev.latest_ping < time_limit:
                    # Push event for all those devices
                    self.event_queue.put(Event(EventType.NO_PING_FOR_LONG, id))
#             no_ping_devices = [id for id, dev in self.devices.items() if dev.latest_ping < time_limit]
#             for id in no_ping_devices:
#                 # Push event for all those devices
#                 self.event_queue.put(Event(EventType.NO_PING_FOR_LONG, id))

    def get_no_ping_time_threshold(self, no_ping_time):
        for i, (threshold, level) in enumerate(self.no_ping_time_thresholds):
            if no_ping_time <= threshold:
                return i - 1
        # If we come here, this means we have passed the last threshold already,
        # This is a special case where we use multiples of the last threshold repeatedly
        return i + int(no_ping_time / threshold) - 1 
    
    def get_no_ping_time_threshold_alert_level(self, index):
        if index < len(self.no_ping_time_thresholds):
            return self.no_ping_time_thresholds[index][1]
        return self.no_ping_time_thresholds[-1][1]
        
    # EVENT HANDLERS
    #----------------
    def handle_voltage_event(self, event_type, device, event_detail):
        device.latest_voltage_level = event_detail
        if device.latest_voltage_level < device.source.voltage_threshold:
            message = 'Module %s current voltage (%.02fV) is under threshold (%.02fV)' % (
                device.source.name, device.latest_voltage_level, device.source.voltage_threshold)
            return Alert(
                level = Alert.LEVEL_WARNING,
                alert_type = AlertType.DEVICE_VOLTAGE_UNDER_THRESHOLD,
                message = message)
        else:
            return None

    def check_code(self, device, event_detail):
        if self.lock_code != event_detail:
            message = 'Bad code typed on module %s' % device.source.name
            return Alert(
                level = Alert.LEVEL_WARNING,
                alert_type = AlertType.WRONG_LOCK_CODE,
                message = message)
        else:
            return None

    def create_lock_event(self, status, alert_type, message = None):
        self.status = status
        self.devices_manager.set_status(self.status)
        return Alert(
            level = Alert.LEVEL_INFO, 
            alert_type = alert_type,
            message = message)
        
    def handle_lock_event(self, event_type, device, event_detail):
        return (self.check_code(device, event_detail) or 
            self.create_lock_event(AlarmStatus.LOCKED, AlertType.LOCK))
    
    def handle_unlock_event(self, event_type, device, event_detail):
        return (self.check_code(device, event_detail) or
            self.create_lock_event(AlarmStatus.UNLOCKED, AlertType.UNLOCK))
    
    def handle_no_ping_for_long(self, event_type, device, event_detail):
        threshold = device.latest_ping_alert_threshold
        no_ping_time = time() - device.latest_ping
        new_threshold = self.get_no_ping_time_threshold(no_ping_time)
        device.latest_ping_alert_threshold = new_threshold
        # First check if alert condition has disappeared or has not changed
        if new_threshold <= threshold:
            return None
        # We have passed a new threshold, we must generate an alert of appropriate level
        level = self.get_no_ping_time_threshold_alert_level(new_threshold)
        message = 'Module %s has provided no presence signal for %.0f seconds' % (
            device.source.name, no_ping_time)
        return Alert(
            level = level,
            alert_type = AlertType.DEVICE_NO_PING_FOR_TOO_LONG,
            message = message)
    
    def check_events(self):
        while True:
            event = self.event_queue.get()
            # Detect stop condition
            if event.event_type == EventType.STOP:
                return
            device = self.devices[event.device_id] if event.device_id else None
            if device and event.event_type != EventType.NO_PING_FOR_LONG:
                device.latest_ping = event.timestamp
                device.latest_ping_alert_threshold = -1
            # Check event type and decide what to do with it
            handler = self.handlers.get(event.event_type, None)
            if handler:
                alert = handler(event.event_type, device, event.detail)
                if alert:
                    alert.when = datetime.fromtimestamp(event.timestamp)
                    alert.config_id = self.config_id
                    alert.device_id = event.device_id
                    self.store_alert(alert)

