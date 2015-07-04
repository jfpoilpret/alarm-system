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
        self.latest_voltage_level = None

#TODO Add monitoring of device pings and generate alerts if no ping during a given time...
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
        self.status = AlarmStatus.LOCKED
        self.config_id = config.id
        # Store lock code from config
        self.lock_code = config.lockcode
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
    
    #FIXME should we clone each device under locking (multi-thread!!!)
    def get_devices(self):
        return self.devices

    def store_alert(self, alert):
        with self.app.app_context():
            db.session.add(alert)
            db.session.commit()
    
    #TODO improve by setting additional info to device for further generation of alerts
    # (eg time without ping)
    def check_pings(self):
        while not self.ping_checker_stop.is_set():
            # Perform check every 1 second
            self.ping_checker_stop.wait(1.0)
            if not self.active:
                return
            # Check list of all devices where last ping > 6 seconds
            #TODO that should be configurable!
            time_limit = time() - 6.0
            #FIXME how to deal with devices that have not been connected yet (time = 0)?
            no_ping_devices = [id for id, dev in self.devices.items() if dev.latest_ping < time_limit]
            for id in no_ping_devices:
                # Push event for all those devices
                self.event_queue.put(Event(EventType.NO_PING_FOR_LONG, id))
    
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

    def create_lock_event(self, status, alert_type):
        self.status = status
        self.devices_manager.set_status(self.status)
        return Alert(
            level = Alert.LEVEL_INFO, 
            alert_type = alert_type)
        
    def handle_lock_event(self, event_type, device, event_detail):
        alert = self.check_code(device, event_detail)
        if alert:
            return alert
        else:
            return self.create_lock_event(AlarmStatus.LOCKED, AlertType.LOCK)
    
    def handle_unlock_event(self, event_type, device, event_detail):
        alert = self.check_code(device, event_detail)
        if alert:
            return alert
        else:
            return self.create_lock_event(AlarmStatus.UNLOCKED, AlertType.UNLOCK)
    
    #TODO improve alerts by generating several levels of alerts based on duration without ping
    #TODO also we should not insert alerts every second but 'aggregate' consecutive alerts into 
    # one every XX seconds...
    def handle_no_ping_for_long(self, event_type, device, event_detail):
        message = 'Module %s has provided no presence signal for %d seconds' % (
            device.source.name, device.latest_ping - time())
        return Alert(
            level = Alert.LEVEL_WARNING,
            alert_type = AlertType.DEVICE_NO_PING_FOR_TOO_LONG,
            message = message)
    
    def check_events(self):
        while True:
            event = self.event_queue.get()
            # Detect stop condition
            if event.event_type == EventType.STOP:
                return
            if event.device_id:
                device = self.devices[event.device_id]
                device.latest_ping = event.timestamp
            else:
                device = None
            # Check event type and decide what to do with it
            handler = self.handlers.get(event.event_type, None)
            if handler:
                alert = handler(event.event_type, device, event.detail)
                if alert:
                    alert.when = datetime.fromtimestamp(event.timestamp)
                    alert.config_id = self.config_id
                    if device:
                        alert.device_id = device.source.id
                    self.store_alert(alert)

