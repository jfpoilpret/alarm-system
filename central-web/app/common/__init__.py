from re import compile
from flask import g
from flask_restful import abort
from app.models import Device, Account
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

ROLES = [
    (Account.ROLE_ADMINISTRATOR, 'Administrator'),
    (Account.ROLE_CONFIGURATOR, 'Configurator'),
    (Account.ROLE_ALARM_SETTER, 'Alarm Setter'),
    (Account.ROLE_ALARM_VIEWER, 'Alarm Viewer'),
]

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

# Authorization checks
#----------------------
def check_admin():
    if not g.user.is_admin():
        abort(401, message = 'You are not allowed to perform this action, only an administrator can!')

def check_configurator():
    if not g.user.is_configurator():
        abort(401, 
            message = 'You are not allowed to perform this action; you must be an administrator or configurator!')

def check_alarm_setter():
    if not g.user.is_alarm_setter():
        abort(401, 
            message = 'You are not allowed to perform this action; you must be at least an alarm setter!')

# SGV utilities
#---------------
VIEWBOX_REGEX = compile(r"\-?[0-9]+")
def extract_viewbox(root):
    view_box = root['@viewBox']
    return [int(x) for x in VIEWBOX_REGEX.findall(view_box)]

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
        if not isinstance(layers, list):
            layers = [layers]
            root['g'] = layers
    else:
        #FIXME if no <g> then shall put everything within <svg> into a new <g>!
        layers = []
        root['g'] = layers
    return dimensions
