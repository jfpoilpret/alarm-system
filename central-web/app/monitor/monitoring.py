# encoding: utf-8
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from threading import Thread
from threading import Event as ThreadEvent
from datetime import datetime
from time import time

class AlarmStatus(object):
    LOCKED = 1
    UNLOCKED = 2
    
from app import db
from app.models import Alert, AlertType
from app.monitor.events import Event, EventType
from app.monitor.network import DevicesManager, DevicesManagerSimulator

monitoring_manager = None

class LiveDevice(object):
    def __init__(self, device):
        self.source = device.detached()
        self.latest_ping = time() - 0.5
        self.latest_ping_alert_threshold = -1
        self.latest_ping_alert_level = None
        self.latest_voltage_level = None
        self.latest_voltage_alert_threshold = -1
        self.latest_voltage_alert_time = None
        self.latest_voltage_alert_level = None

class MonitoringManager(object):
    instance = None
    
    @staticmethod
    def create(app):
        MonitoringManager.instance = MonitoringManager(app)
        return MonitoringManager.instance
    
    def __init__(self, app):
        self.handlers = {
            EventType.VOLTAGE: self._handle_voltage_event,
            EventType.LOCK_CODE: self._handle_lock_event,
            EventType.UNLOCK_CODE: self._handle_unlock_event,
            EventType.NO_PING_FOR_LONG: self._handle_no_ping_for_long
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
        # Deactivate if already active
        self.deactivate()
        self.status = AlarmStatus.UNLOCKED
        self.config_id = config.id
        # Store lock code from config
        self.lock_code = config.lockcode
        # Get alerts thresholds from config
        # Alerts after some time without ping
        # Format is (time, level)
        # where time is the time (in seconds) during which the device has not pinged
        # An alert of the given level is emitted each time a new time threshold is reached
        # When the last threshold has been reached, the same alert is repeated once every 
        # "time" has elapsed
        self.no_ping_time_thresholds = [(float(entry.alert_time), entry.alert_level) for entry in config.no_ping_time_alert_thresholds]
        self.no_ping_time_thresholds = sorted(self.no_ping_time_thresholds, key = lambda x: x[0], reverse = False)
        # Ensure list is never empty
        if len(self.no_ping_time_thresholds) == 0:
            self.no_ping_time_thresholds = [(10.0, Alert.LEVEL_WARNING)]
        # Alerts when device voltage under some rate wrt device voltage threshold
        # Format is (ratio, level, period)
        # Whenever the ratio of voltage level over a device voltage threshold becomes under ratio,
        # an alert of the given level is emitted, if after period (minutes) the actual ratio is still
        # under the same ratio, the same alert is emitted again.
        self.voltage_alert_thresholds = [(entry.voltage_rate/100.0, entry.alert_level, entry.alert_time * 60.0) for entry in config.voltage_rate_alert_thresholds]
        self.voltage_alert_thresholds = sorted(self.voltage_alert_thresholds, key = lambda x: x[0], reverse = True)
        # Ensure list is never empty
        if len(self.voltage_alert_thresholds) == 0:
            self.voltage_alert_thresholds = [(0.99, Alert.LEVEL_INFO, 600.0)]
        # Create dictionary of LiveDevices from config
        self.devices = {id: LiveDevice(device) for id, device in config.devices.items()}
        # Start thread that reads queues and act upon received messages (DB, SMS...)
        # Create the event queue that will be used by DevicesManager
        self.event_queue = Queue()
        self.event_checker = Thread(target = self._check_events)
        self.event_checker.start()
        self.active = True
        # Start _check_pings thread
        self.ping_checker_stop.clear()
        self.ping_checker = Thread(target = self._check_pings)
        self.ping_checker.start()

        # Instantiate DevicesManager (based on app.config)
        self.devices_manager = self.devices_manager_class(self.event_queue, self.devices)
        
        # Create info alert
        self._store_alert(Alert(
            config_id = self.config_id,
            when = datetime.fromtimestamp(time()),
            level = Alert.LEVEL_INFO,
            alert_type = AlertType.SYSTEM_ACTIVATION,
            message = 'System activated',
            device = None), need_context = False)
    
    def deactivate(self):
        if self.event_checker:
            # Stop DevicesManager
            self.devices_manager.deactivate()
            self.devices_manager = None
            # Then stop thread by sending special event to queue
            self.event_queue.put(Event(EventType.STOP))
            # Wait until thread is finished
            self.event_checker.join()
            self.event_checker = None
            # Wait for _check_pings() thread to stop
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
            self._store_alert(Alert(
                config_id = config_id,
                when = datetime.fromtimestamp(time()),
                level = Alert.LEVEL_INFO,
                alert_type = AlertType.SYSTEM_DEACTIVATION,
                message = 'System deactivated',
                device = None), need_context = False)
    
    def lock(self):
        alert = self._create_lock_event(
            AlarmStatus.LOCKED, AlertType.LOCK, 'Lock through monitoring application')
        alert.when = datetime.fromtimestamp(time())
        alert.config_id = self.config_id
        self._store_alert(alert, need_context = False)
    
    def unlock(self):
        alert = self._create_lock_event(
            AlarmStatus.UNLOCKED, AlertType.UNLOCK, 'Unlock through monitoring application')
        alert.when = datetime.fromtimestamp(time())
        alert.config_id = self.config_id
        self._store_alert(alert, need_context =  False)
    
    def get_status(self):
        return self.status
    
    #FIXME should we clone each device under locking (multi-thread!!!)
    def get_devices(self):
        return self.devices

    def _store_alert(self, alert, need_context = True):
        if need_context:
            with self.app.app_context():
                db.session.add(alert)
                db.session.commit()
        else:
            db.session.add(alert)
            db.session.commit()
    
    def _check_pings(self):
        while not self.ping_checker_stop.is_set():
            # Perform check every 1 second
            self.ping_checker_stop.wait(1.0)
            if not self.active:
                return
            # Check list of all devices where last ping > 6 seconds
            time_limit = time() - self.no_ping_time_thresholds[0][0]
            for id, dev in self.devices.items():
                if dev.latest_ping < time_limit:
                    # Push event for all those devices
                    self.event_queue.put(Event(EventType.NO_PING_FOR_LONG, id))
                else:
                    dev.latest_ping_alert_level = None

    def _get_no_ping_time_threshold(self, no_ping_time):
        for i, (threshold, _) in enumerate(self.no_ping_time_thresholds):
            if no_ping_time <= threshold:
                return i - 1
        # If we come here, this means we have passed the last threshold already,
        # This is a special case where we use multiples of the last threshold repeatedly
        return i + int(no_ping_time / threshold) - 1 
    
    def _get_no_ping_time_threshold_alert_level(self, index):
        if index < 0:
            return None
        if index < len(self.no_ping_time_thresholds):
            return self.no_ping_time_thresholds[index][1]
        return self.no_ping_time_thresholds[-1][1]
        
    def _get_voltage_alert_threshold(self, ratio):
        for i, (rate, _, _) in enumerate(self.voltage_alert_thresholds):
            if ratio >= rate:
                return i - 1
        # If we come here, this means we have passed the last rate already
        return i
    
    # EVENT HANDLERS
    #----------------
    def _handle_voltage_event(self, event_type, device, event_detail):
        device.latest_voltage_level = event_detail
        old_threshold = device.latest_voltage_alert_threshold
        rate = device.latest_voltage_level / device.source.voltage_threshold
        new_threshold = self._get_voltage_alert_threshold(rate)
        device.latest_voltage_alert_threshold = new_threshold
        if new_threshold == -1:
            # Reset last alert time
            device.latest_voltage_alert_time = None
            device.latest_voltage_alert_level = None
            return None
        
        alert_threshold = self.voltage_alert_thresholds[new_threshold]
        level = alert_threshold[1]
        now = time()
        device.latest_voltage_alert_level = level
        if new_threshold <= old_threshold:
            # Check if we need to re-send the alarm (based on last time)
            delay = now - device.latest_voltage_alert_time if device.latest_voltage_alert_time else 0.0
            if delay < alert_threshold[2]:
                return None
        device.latest_voltage_alert_time = now
        message = 'Module %s current voltage (%.02fV) is under threshold (%.02fV)' % (
            device.source.name, device.latest_voltage_level, device.source.voltage_threshold)
        return Alert(
            level = level,
            alert_type = AlertType.DEVICE_VOLTAGE_UNDER_THRESHOLD,
            message = message)

    def _check_code(self, device, event_detail):
        if self.lock_code != event_detail:
            message = 'Bad code typed on module %s' % device.source.name
            return Alert(
                level = Alert.LEVEL_WARNING,
                alert_type = AlertType.WRONG_LOCK_CODE,
                message = message)
        else:
            return None

    def _create_lock_event(self, status, alert_type, message = None):
        self.status = status
        self.devices_manager.set_status(self.status)
        return Alert(
            level = Alert.LEVEL_INFO, 
            alert_type = alert_type,
            message = message)
        
    def _handle_lock_event(self, event_type, device, event_detail):
        return (self._check_code(device, event_detail) or 
            self._create_lock_event(AlarmStatus.LOCKED, AlertType.LOCK))
    
    def _handle_unlock_event(self, event_type, device, event_detail):
        return (self._check_code(device, event_detail) or
            self._create_lock_event(AlarmStatus.UNLOCKED, AlertType.UNLOCK))
    
    def _handle_no_ping_for_long(self, event_type, device, event_detail):
        old_threshold = device.latest_ping_alert_threshold
        no_ping_time = time() - device.latest_ping
        new_threshold = self._get_no_ping_time_threshold(no_ping_time)
        device.latest_ping_alert_threshold = new_threshold
        level = self._get_no_ping_time_threshold_alert_level(new_threshold)
        device.latest_ping_alert_level = level
        # First check if alert condition has disappeared or has not changed
        if new_threshold <= old_threshold:
            return None
        # We have passed a new threshold, we must generate an alert of appropriate level
        message = 'Module %s has provided no presence signal for %.0f seconds' % (
            device.source.name, no_ping_time)
        return Alert(
            level = level,
            alert_type = AlertType.DEVICE_NO_PING_FOR_TOO_LONG,
            message = message)
    
    def _check_events(self):
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
                    if device:
                        alert.device_id = device.source.id
                    self._store_alert(alert)
