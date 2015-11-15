# encoding: utf-8

class AbstractDevicesManager(object):
    def __init__(self, queue, devices, code = None, status = None):
        self.queue = queue
        self.devices = devices
        self.code = code
        self.status = status

    def exit(self):
        pass
    
    def deactivate(self):
        pass
    
    def set_status(self, status):
        self.status = status

    def set_code(self, code):
        self.code = code
