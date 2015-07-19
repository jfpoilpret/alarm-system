from re import compile
from flask import abort, jsonify, render_template, session, url_for
from flask_login import current_user
from app.models import Device
from xmltodict import parse, unparse
from unittest.test.testmock.support import is_instance
from wtforms.fields.core import IntegerField
from wtforms.widgets.core import HiddenInput

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

# WTF Form Utilities
#--------------------
class HiddenInteger(IntegerField):
    widget = HiddenInput()

# AJAX form validation
#----------------------
def pre_check(form, return_none_if_ok = False, use_flash_for_errors = True):
    # Check form is valid
    if not form.validate():
        if use_flash_for_errors:
            # Get list of fields in error
            fields = list(form.errors.keys())
            # Get all error messages and remove duplicates
            messages = {error for errors in form.errors.values() for error in errors}
            # Format all error messages as flash messages
            flash_messages = '\n'.join([render_template(
                'flash_messages.html', message = message, category = 'warning') for message in messages])
            return jsonify(result = 'ERROR', fields = fields, flash_messages = flash_messages)
        else:
            #TODO
            fields = {field: render_template('field_errors.html', errors = list(errors)) for field, errors in form.errors.items()}
            return jsonify(result = 'ERROR', fields = fields, flash_messages = [])
    return None if return_none_if_ok else jsonify(result = 'OK')

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
    view_box = root['@viewBox']
    return [int(x) for x in VIEWBOX_REGEX.findall(view_box)]

def extract_viewbox_from_config(config):
    svg_xml = parse(config.map_area, process_namespaces = False)
    root = svg_xml['svg']
    return extract_viewbox(root)

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
def prepare_map(config, update_device_image, update_device_group):
    svg_xml = parse(config.map_area, process_namespaces = False)
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
                '@stroke-width': '3',
                '@fill': 'red',
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
    return unparse(svg_xml, full_document = False)

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
def prepare_map_for_config(config):
    def update_image(device_image):
        device_image['@onmousedown'] = 'startDrag(evt)'
        device_image['@onmousemove'] = 'drag(evt)'
        device_image['@onmouseup'] = 'endDrag(evt)'
    def update_group(device_group):
        device_group['@class'] = 'device-image'
    return prepare_map(config, update_image, update_group)

# This function reads an SVG string (XML) containing the monitoring zone map,
# adds a layer for devices, and prepares the result for direct SVG embedding to HTML
def prepare_map_for_monitoring(config):
    def update_image(device_image):
        device_image['@class'] = 'ping-alert-0 voltage-alert-0'
    def update_group(device_group):
        device_group['@class'] = 'monitor-device-image'
    return prepare_map(config, update_image, update_group)
