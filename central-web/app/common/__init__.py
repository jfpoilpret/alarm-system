from re import compile
from flask import abort, session, url_for
from flask_login import current_user
from app.models import Device
from xmltodict import parse, unparse
from unittest.test.testmock.support import is_instance

# Common constants
#------------------
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

# Authorization checks
#----------------------
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

# URL utilities
#---------------
def get_return_url():
    url = session.get('return_url', None)
    if url:
        return url
    elif current_user.is_configurator():
        return url_for('configure.home')
    else:
        return url_for('monitor.home')

# SGV utilities
#---------------
VIEWBOX_REGEX = compile(r"\-?[0-9]+")
def extract_viewbox(root):
    viewBox = root['@viewBox']
    return [int(x) for x in VIEWBOX_REGEX.findall(viewBox)]

def extract_viewbox_from_config(config):
    svgXml = parse(config.map_area, process_namespaces = False)
    root = svgXml['svg']
    return extract_viewbox(root)

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
# devices is an array of objects that contain location (and later device image somehow)
def prepare_map_for_config(config):
    svgXml = parse(config.map_area, process_namespaces = False)
    root = svgXml['svg']
    root['@id'] = 'svgMap'
    # parse viewBox to find out coordinates to use for additional layer
    dimensions = extract_viewbox(root)
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
                '@data-toggle': 'popover',
                '@title': 'Module ID %d' % id,
                '@data-content': device.name,
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

#TODO refactor common parts with prepare_map_for_config() above
# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
# devices is an array of objects that contain location (and later device image somehow)
def prepare_map_for_monitoring(config):
    svgXml = parse(config.map_area, process_namespaces = False)
    root = svgXml['svg']
    root['@id'] = 'svgMap'
    # parse viewBox to find out coordinates to use for additional layer
    dimensions = extract_viewbox(root)
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
                '@data-toggle': 'popover',
                '@title': 'Module ID %d' % id,
                '@data-content': device.name
            }
            device_group = {
                '@id': 'device-%d' % id,
                '@class': 'monitor-device-image',
                'circle': device_image
            }
            layers.append(device_group)
    return unparse(svgXml, full_document = False)
