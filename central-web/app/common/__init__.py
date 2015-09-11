from re import compile
from flask import abort, g, jsonify, session, url_for
from app.models import Device
from xmltodict import parse, unparse
from unittest.test.testmock.support import is_instance
from wtforms.fields.core import IntegerField
from wtforms.widgets.core import HiddenInput
from flask_restful.fields import Raw
from datetime import datetime

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

# Webargs utilities
#-------------------

# 'use' functions
trim = lambda s: s.strip()

def label_to_code(code_label_pairs):
    def convert(input_label):
        for (code, label) in code_label_pairs:
            if input_label == label:
                return code
        return None
    return convert

DEFAULT_DATE_FORMAT = '%d-%m-%Y'

def string_to_date(format = DEFAULT_DATE_FORMAT):
    def convert(input):
        return datetime.strptime(input, format) if input else None
    return convert

# 'validate' functions
def choices(*args):
    return lambda v: v in args

def boolean():
    return label_to_code([(True, 'true'), (False, 'false')])

# Flask-RestFul marshalling utilities
#-------------------------------------
class CodeToLabelField(Raw):
    def __init__(self, code_label_pairs, default = None, attribute = None):
        Raw.__init__(self, default, attribute)
        self.code_label_pairs = code_label_pairs

    def format(self, value):
        for (code, label) in self.code_label_pairs:
            if value == code:
                return label
        return None

# Authentication for REST services
#----------------------------------


# Authorization checks
#----------------------
def check_admin():
    if not g.user or not g.user.is_admin():
        abort(401, message = 'You are not allowed to perform this action, only an administrator can!')

def check_configurator():
    if not g.user or g.user.is_configurator():
        abort(401, 
            message = 'You are not allowed to perform this action; you must be an administrator or configurator!')

def check_alarm_setter():
    if not g.user or g.user.is_alarm_setter():
        abort(401, 
            message = 'You are not allowed to perform this action; you must be at least an alarm setter!')

# SGV utilities
#---------------
#TODO refactor what's not really common and put where it belongs!
VIEWBOX_REGEX = compile(r"\-?[0-9]+")
def extract_viewbox(root):
    view_box = root['@viewBox']
    return [int(x) for x in VIEWBOX_REGEX.findall(view_box)]

def extract_viewbox_from_config(config):
    svg_xml = parse(config.map_area, process_namespaces = False)
    root = svg_xml['svg']
    return extract_viewbox(root)

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
def prepare_map(svg_xml):
    root = svg_xml['svg']
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
        #FIXME if no <g> then shall put everything within <svg> into a new <g>!
        layers = []
        root['g'] = layers
    return dimensions

def prepare_devices(devices, layers, dimensions, update_device_image, update_device_group):
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
                '@stroke-width': '3',
                '@fill': 'red',
                '@data-uri': url_for('.device', id = device.id),
                '@data-toggle': 'popover',
                '@title': 'Module %s (ID %d)' % (device.name, id),
                '@data-content': ''
            }
            update_device_image(device_image)
            device_group = {
                '@id': 'device-%d' % id,
                'circle': device_image
            }
            update_device_group(device_group)
            layers.append(device_group)

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
def prepare_map_for_config(config):
    def update_image(device_image):
        device_image['@onmousedown'] = 'startDrag(evt)'
        device_image['@onmousemove'] = 'drag(evt)'
        device_image['@onmouseup'] = 'endDrag(evt)'
    def update_group(device_group):
        device_group['@class'] = 'device-image'
    svg_xml = parse(config.map_area, process_namespaces = False)
    dimensions = prepare_map(svg_xml)
    prepare_devices(config.devices, svg_xml['svg']['g'], dimensions, update_image, update_group)
    return unparse(svg_xml, full_document = False)

def prepare_device(device, dimensions):
    return {
        'id': device.device_id,
        'name': device.name,
        'x': (device.location_x or 0.5) * dimensions[2] + dimensions[0],
        'y': (device.location_y or 0.5) * dimensions[3] + dimensions[1]
    }

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
def prepare_map_for_monitoring(config):
    svg_xml = parse(config.map_area, process_namespaces = False)
    dimensions = prepare_map(svg_xml)
    # Get width/height/viewBox
    svg = svg_xml['svg']
    # Prepare all devices for client rendering
    devices = [prepare_device(device, dimensions) for device in config.devices.values()]
    return { 
        'map': unparse(svg_xml['svg']['g'][0], full_document = False),
        'width': svg['@width'],
        'height': svg['@height'],
        'viewBox': svg['@viewBox'],
        'r': 0.02 * dimensions[2],
        'devices': devices
    }
