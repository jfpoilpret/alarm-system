from threading import Thread

#TODO
class AbstractDevicesManager:
    def __init__(self, queue, devices, status = None):
        self.queue = queue
        self.devices = devices
        self.status = status

    def deactivate(self):
        pass
    
    def set_status(self, status):
        self.status = status

class DevicesManagerSimulator(AbstractDevicesManager, Thread):
    def run(self):
        #TODO simulate events randomly, ensure that we also trigger alarm conditions
        pass


#TODO later 
class DevicesManager(AbstractDevicesManager):
    pass
