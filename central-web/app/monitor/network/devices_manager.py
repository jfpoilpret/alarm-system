# encoding: utf-8

from threading import Thread
from threading import Event as ThreadEvent
import zmq

from app.monitor.network.message_handlers import PingHandler, VoltageHandler, LockUnlockHandler
from app.monitor.network.common_devices_manager import AbstractDevicesManager
from app.models import Device
from app.monitor.monitoring import AlarmStatus

class DevicesManager(AbstractDevicesManager, Thread):
    # RF Communication constants
    NETWORK = 0xC05A
    SERVER_ID = 0x01
    # Timing constants
    PERIOD_REFRESH_KEY_SECS = 120.0

    def __init__(self, *args, **kwargs):
        AbstractDevicesManager.__init__(self, *args, **kwargs)
        Thread.__init__(self)
        #TODO Launch process to handle devices communication through NRF24
        # RFManager should be launched earlier (at web system init time)
        
        # Start ZMQ sockets to handle communication with Collector process
        context = zmq.Context.instance()
        self.command = context.socket(zmq.REQ)
        self.command.connect("ipc:///tmp/alarm-system/command.ipc")
        self.data = context.socket(zmq.SUB)
        self.data.connect("ipc:///tmp/alarm-system/devices.ipc")
        self.data.setsockopt_string(zmq.SUBSCRIBE, "")
        
        # Setup RF message handlers
        #TODO review handler design (as messages come from collector process now)
        pingHandler = PingHandler()
        voltageHandler = VoltageHandler()
        lockHandler = LockUnlockHandler()
        self.handlers = {
            'LOCK': lockHandler,
            'UNLOCK': lockHandler,
            'PING': pingHandler,
            'VOLT': voltageHandler
        }
        self.stop = ThreadEvent()
        self.stop.clear()
        self.start()

    def set_code(self, code):
        AbstractDevicesManager.set_code(self, code)
        self.send_command('CODE %s' % code)
    
    def exit(self):
        self.send_command('EXIT')
    
    def set_status(self, status):
        AbstractDevicesManager.set_status(self, status)
        self.send_command('LOCK' if status == AlarmStatus.LOCKED else 'UNLOCK')
        
    def get_rf_status(self):
        # Parse get low-level RF status from RFManager
        result = self.send_command('STATE', False)
        # Parse result
        values = [int(s) for s in result.split() if s.isdigit()]
        return values[0], values[1], values[2], values[3]
    
    def send_command(self, command, check_ok = True):
        print(command)
        #self.command.send(command.encode('ascii'))
        self.command.send_string(command)
        result = self.command.recv_string()
        print(result)
        if check_ok:
            return result == "OK"
        else:
            return result
    
    def deactivate(self):
        self.stop.set()
        self.join()

    def run(self):
        # Initialize and start RFManager
        cmd = "INIT %x %x %f" % (
            DevicesManager.NETWORK, DevicesManager.SERVER_ID, DevicesManager.PERIOD_REFRESH_KEY_SECS)
        for id, device in self.devices.items():
            if device.source.kind == Device.KIND_KEYPAD:
                cmd += " %x" % id
        self.send_command(cmd)
        self.send_command('CODE %s' % self.code)
        self.send_command("START")
        while True:
            #FIXME try/except EAGAIN or use timeout?
            try:
                message = self.data.recv_string(zmq.NOBLOCK)
                if message:
                    event = self.handle_message(message)
                    if event:
                        self.queue.put(event)
            except zmq.Again:
                pass
            if self.stop.is_set():
                break
        self.send_command("STOP")
    
    def handle_message(self, message):
        # Parse message: ID TS VERB [ARGS]
        args = message.split(' ')
        id = int(args[0])
        ts = int(args[1])
        verb = args[2]
        args = args[3:] if len(args) > 2 else []
        #if self.devices.has_key(id):
        if id in self.devices:
            device = self.devices[id]
            handler = self.handlers.get(verb)
            if handler:
                return handler(verb, ts, id, device, args)
            else:
                print("Source %02x, unknown verb %s!" % (id, verb))
                return None
        else:
            print("Unknown source %02x (verb %s)!" % (id, verb))
            return None
    
