from re import compile
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

VIEWBOX_REGEX = compile(r"\-?[0-9]+")
def extractViewBox(root):
    viewBox = root['@viewBox']
    return [int(x) for x in VIEWBOX_REGEX.findall(viewBox)]

def extractSvgViewBox(config):
    svgXml = parse(config.map_area, process_namespaces = False)
    root = svgXml['svg']
    return extractViewBox(root)

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
# devices is an array of objects that contain location (and later device image somehow)
def prepareMap(config):
    svgXml = parse(config.map_area, process_namespaces = False)
    root = svgXml['svg']
    root['@id'] = 'svgMap'
    # parse viewBox to find out coordinates to use for additional layer
    dimensions = extractViewBox(root)
    root['@width'] = '100%'
    root['@height'] = '100%'
    # Ensure we have SVG groups present so that we can add to them
    if 'g' in root:
        layers = root['g']
        if not is_instance(layers, list):
            layers = [layers]
            root['g'] = layers
    else:
        layers = []
        root['g'] = layers
        
    #FIXME drag/drop not fully smooth?
    #TODO add save devices location button (javascript?)
    #TODO add tooltip (javascript?) to each device
    devices = config.devices
    if len(devices) > 0:
        for id, device in devices.items():
            x = (device.location_x or 0.5) * dimensions[2] + dimensions[0]
            y = (device.location_y or 0.5) * dimensions[3] + dimensions[1]
            r = 0.02 * dimensions[2]
            device_image = {
                '@cx': str(x),
                '@cy': str(y),
                '@r': str(r),
                '@stroke': 'red',
                '@fill': 'red',
                '@title': device.name,
                '@onmousedown': 'startDrag(evt)',
                '@onmousemove': 'drag(evt)',
                '@onmouseup': 'endDrag(evt)',
            }
            device_group = {
                '@id': 'device-%d' % id,
                '@class': 'device-image',
                'circle': device_image
            }
            layers.append(device_group)
    return unparse(svgXml, full_document = False)
