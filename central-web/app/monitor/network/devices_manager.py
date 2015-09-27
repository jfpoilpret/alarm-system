# encoding: utf-8

from threading import Thread
from threading import Event as ThreadEvent
from app.monitor.network.message_handlers import PingHandler, VoltageHandler, LockUnlockHandler
from app.monitor.network.message import MessageType
from app.monitor.nrf24.nrf24 import NRF24
from datetime import time
from app.monitor.network.common_devices_manager import AbstractDevicesManager
from app.monitor.cipher.cipher import XTEA

class RF(NRF24):
    def send(self, device, port, payload):
        now = time.time()
        count = super(RF, self).send(device, port, payload)
        print("Send time = %.02f ms" % ((time.time() - now) * 1000.0))
        return count

class DevicesManager(AbstractDevicesManager, Thread):
    # RF Communication constants
    NETWORK = 0xC05A
    SERVER_ID = 0x01
    # Hardware constants
    CE_PIN = 25
    # Timing constants
    PERIOD_REFRESH_KEY_SECS = 120.0

    def __init__(self, *args, **kwargs):
        AbstractDevicesManager.__init__(self, *args, **kwargs)
        Thread.__init__(self)
        # Prepare devices for RF messages (create cipher)
        for device in self.devices.values():
            device.cipher = XTEA()
            device.next_key_time = 0
        # Initialize RF device
        self.nrf = RF(DevicesManager.NETWORK, DevicesManager.SERVER_ID)
        # TODO rework handlers to return an Event to be sent 
        pingHandler = PingHandler(self, DevicesManager.PERIOD_REFRESH_KEY_SECS)
        voltageHandler = VoltageHandler()
        lockHandler = LockUnlockHandler(self)
        self.handlers = {
            MessageType.LOCK_CODE: lockHandler,
            MessageType.UNLOCK_CODE: lockHandler,
            MessageType.PING_SERVER: pingHandler,
            MessageType.VOLTAGE_LEVEL: voltageHandler
        }
        self.stop = ThreadEvent()
        self.stop.clear()
        self.start()

    def deactivate(self):
        self.stop.set()
        self.join()

    def run(self):
        self.nrf.begin(0, 0, DevicesManager.CE_PIN)
        while True:
            # Print some RF status
            print('NRF24 trans = %d, retrans = %d, drops = %d' % (
                self.nrf.get_trans(), self.nrf.get_retrans(), self.nrf.get_drops()))
            # Wait for remote modules calls (or until config is deactivated)
            payload = self.nrf.recv(self.stop.wait)
            if self.stop.is_set():
                return
            if payload:
                now = time.time()
                event = self.handle_message(payload)
                print("Total time = %.02f ms" % ((time.time() - now) * 1000.0))
                if event:
                    self.queue.put(event)
    
    def handle_message(self, payload):
        device = self.devices[payload.device]
        port = payload.port
        handler = self.handlers.get(port)
        if handler:
            return handler(self.nrf, device, port, payload.content)
        else:
            print("Source %02x, unknown port %02x!" % (device.source.device_id, port))
            return None
    