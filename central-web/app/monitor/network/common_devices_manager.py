# encoding: utf-8

class AbstractDevicesManager(object):
    def __init__(self, queue, devices, status = None):
        self.queue = queue
        self.devices = devices
        self.status = status

    def exit(self):
        pass
    
    def deactivate(self):
        pass
    
    def set_status(self, status):
        self.status = status
