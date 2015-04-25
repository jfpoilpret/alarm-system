from flask import abort
from flask_login import current_user
from app.models import Device, Account

class DeviceKind:
    def __init__(self, allowed_ids, threshold = 2.7):
        self.allowed_ids = allowed_ids
        self.threshold = threshold

device_kinds = {
    Device.KIND_KEYPAD: DeviceKind([0x10, 0x11, 0x12, 0x13]),
    Device.KIND_MOTION: DeviceKind(list(range(0x20, 0x30))),
    Device.KIND_CAMERA: DeviceKind(list(range(0x30, 0x38))),
    #TODO later add new modules such as: laser beam, door open detection, smoke detector...
}

def check_admin():
    if current_user.role != Account.ROLE_ADMINISTRATOR:
        abort(401, message = 'You are not allowed to perform this action, only an administrator can!')

def check_configurator():
    if current_user.role not in [Account.ROLE_ADMINISTRATOR, Account.ROLE_CONFIGURATOR]:
        abort(401, 
            message = 'You are not allowed to perform this action; you must be an administrator or configurator!')

def check_alarm_setter():
    if current_user.role not in [Account.ROLE_ADMINISTRATOR, Account.ROLE_CONFIGURATOR, Account.ROLE_ALARM_SETTER]:
        abort(401, 
            message = 'You are not allowed to perform this action; you must be at least an alarm setter!')

