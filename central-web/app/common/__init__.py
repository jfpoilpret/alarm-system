from flask import abort
from flask_login import current_user
from app.models import Device
from xmltodict import parse, unparse
from unittest.test.testmock.support import is_instance

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
    if not current_user.is_admin():
        abort(401, message = 'You are not allowed to perform this action, only an administrator can!')

def check_configurator():
    if not current_user.is_configurator():
        abort(401, 
            message = 'You are not allowed to perform this action; you must be an administrator or configurator!')

def check_alarm_setter():
    if not current_user.is_alarm_setter():
        abort(401, 
            message = 'You are not allowed to perform this action; you must be at least an alarm setter!')

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
# devices is an array of objects that contain location (and later device image somehow)
def prepareMap(svgMap, devices = []):
#    svgXml = parse(svgMap, process_namespaces = True)
    svgXml = parse(svgMap, process_namespaces = False)
    root = svgXml['svg']
    #TODO parse viewBox to find out coordinates to use for additional layer
    viewBox = root['@viewBox']
    root['@width'] = '100%'
    root['@height'] = '100%'
    layers = root['g']
    if not is_instance(layers, list):
        layers = [layers]
        root['g'] = layers
    deviceLayer = {}
#    deviceLayer['rect'] = 
#    layers.append(deviceLayer)
    return unparse(svgXml, full_document = False)
