# encoding: utf-8

from ... import db

from flask_restful import fields, marshal_with, Resource
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs

from app.models import Configuration, Alert, AlertType, Device
from app.common import CodeToLabelField, label_to_code, string_to_date, check_alarm_setter, prepare_map
from app.monitor.monitoring import AlarmStatus, MonitoringManager
from time import time
from datetime import datetime
from xmltodict import parse, unparse

class MonitorStatusResource(Resource):
    CONFIG_FIELDS = {
        'id': fields.Integer,
        'name': fields.String,
        'active': fields.Boolean,
        'locked': fields.Boolean,
        'map': fields.Url('.map', absolute = False),
    }
    
    #TODO validate that active false and locked true not allowed
    CONFIG_ARGS = {
        'active': Arg(bool, required = False),
        'locked': Arg(bool, required = False)
    }

    @marshal_with(CONFIG_FIELDS)
    def get(self):
        config = Configuration.query.filter_by(current = True).first_or_404()
        return self._get_status(config)

    @use_kwargs(CONFIG_ARGS, locations = ['json'])
    @marshal_with(CONFIG_FIELDS)
    def put(self, active, locked):
        check_alarm_setter()
        config = Configuration.query.filter_by(current = True).first_or_404()
        if active is not None and active != config.active:
            config.active = active
            db.session.add(config)
            db.session.commit()
            db.session.refresh(config)
            # Actually activate/deactivate the alarm system
            if active:
                MonitoringManager.instance.activate(config)
            else:
                MonitoringManager.instance.deactivate()
        # For lock change, first verify that config is active
        if config.active:
            currently_locked = (MonitoringManager.instance._get_status() == AlarmStatus.LOCKED)
            if locked is not None and locked != currently_locked:
                if locked:
                    MonitoringManager.instance.lock()
                else:
                    MonitoringManager.instance.unlock()
        return self._get_status(config)

    def _get_status(self, config):
        locked = (MonitoringManager.instance.get_status() == AlarmStatus.LOCKED)
        return {
            'id': config.id,
            'name': config.name,
            'active': config.active, 
            'locked': locked
        }

class MonitorMapResource(Resource):
    DEVICE_FIELDS = {
        'id': fields.Integer,
        'name': fields.String,
        'x': fields.Float,
        'y': fields.Float,
    }
    MAP_FIELDS = {
        'map': fields.String,
        'width': fields.String,
        'height': fields.String,
        'viewBox': fields.String,
        'r': fields.Integer,
        'devices': fields.List(fields.Nested(DEVICE_FIELDS))
    }

    @marshal_with(MAP_FIELDS)
    def get(self):
        config = Configuration.query.filter_by(current = True).first_or_404()
        return self._prepare_map_for_monitoring(config)

    # This function reads an SVG string (XML) containing the monitoring zone map,
    # adds a layer for devices, and prepares the result for direct SVG embedding to HTML
    def _prepare_map_for_monitoring(self, config):
        svg_xml = parse(config.map_area, process_namespaces = False)
        dimensions = prepare_map(svg_xml)
        # Get width/height/viewBox
        svg = svg_xml['svg']
        # Prepare all devices for client rendering
        devices = [self._prepare_device(device, dimensions) for device in config.devices.values()]
        return { 
            'map': unparse(svg_xml['svg']['g'][0], full_document = False),
            'width': svg['@width'],
            'height': svg['@height'],
            'viewBox': svg['@viewBox'],
            'r': 0.02 * dimensions[2],
            'devices': devices
        }

    def _prepare_device(self, device, dimensions):
        return {
            'id': device.device_id,
            'name': device.name,
            'x': (device.location_x or 0.5) * dimensions[2] + dimensions[0],
            'y': (device.location_y or 0.5) * dimensions[3] + dimensions[1]
        }
    

DEVICE_KINDS = [
    (Device.KIND_KEYPAD, 'entry keypad'),
    (Device.KIND_MOTION, 'motion detector'),
    (Device.KIND_CAMERA, 'camera'),
]

ALERT_LEVELS = [
    (Alert.LEVEL_INFO, 'info'),
    (Alert.LEVEL_WARNING, 'warning'),
    (Alert.LEVEL_ALARM, 'alarm'),
]

ALERT_TYPES = [
    (AlertType.DEVICE_NO_PING_FOR_TOO_LONG, 'no-ping'),
    (AlertType.DEVICE_VOLTAGE_UNDER_THRESHOLD, 'voltage-level'),
    (AlertType.LOCK, 'lock'),
    (AlertType.UNLOCK, 'unlock'),
    (AlertType.SYSTEM_ACTIVATION, 'activation'),
    (AlertType.SYSTEM_DEACTIVATION, 'deactivation'),
    (AlertType.WRONG_LOCK_CODE, 'wrong-code'),
]

class MonitorAlertsResource(Resource):
    DEVICE_FIELDS = {
        'id': fields.Integer,
        'name': fields.String,
        'kind': CodeToLabelField(DEVICE_KINDS),
        'device_id': fields.Integer
    }
    
    ALERT_FIELDS = {
        'id': fields.Integer,
        'when': fields.DateTime(dt_format = 'iso8601'),
        'level': CodeToLabelField(ALERT_LEVELS),
        'alert_type': CodeToLabelField(ALERT_TYPES),
        'message': fields.String,
        'device': fields.Nested(DEVICE_FIELDS)
    }

    #TODO allow multiple alert levels and types
    ALERT_GET_ARGS = {
        'since_id': Arg(int, required = False, allow_missing = True),
        'max_count': Arg(int, required = False, default = 100),
        'period_from': Arg(required = False, use = string_to_date(), allow_missing = True),
        'period_to': Arg(required = False, use = string_to_date(), allow_missing = True),
        'alert_level': Arg(int, required = False, use = label_to_code(ALERT_LEVELS), allow_missing = True),
        'alert_type': Arg(int, required = False, use = label_to_code(ALERT_TYPES), allow_missing = True),
    }

    @use_args(ALERT_GET_ARGS, locations = ['query'])
    @marshal_with(ALERT_FIELDS)
    def get(self, args):
        # Find current configuration
        current_config = Configuration.query.filter_by(current = True).first_or_404()
        # Build query based on passed arguments
        query = Alert.query.filter_by(config_id = current_config.id)
        if 'since_id' in args and args['since_id']:
            query = query.filter(Alert.id > args['since_id'])
        if 'period_from' in args and args['period_from']:
            query = query.filter(Alert.when >= args['period_from'])
        if 'period_to' in args and args['period_to']:
            query = query.filter(Alert.when <= args['period_to'])
        if 'alert_level' in args and args['alert_level']:
            query = query.filter_by(level = args['alert_level'])
        if 'alert_type' in args and args['alert_type']:
            query = query.filter_by(alert_type = args['alert_type'])
#         query = query.order_by(Alert.when.desc())
        query = query.order_by(Alert.id.desc())
        # Limit number of retrieved records
        if 'max_count' in args and args['max_count']:
            query = query.limit(args['max_count'])
        return query.all()
    
    #TODO allow more filters: levels/types of alerts
    ALERT_DELETE_ARGS = {
        'clear_until': Arg(required = False, use = string_to_date()),
    }

    @use_kwargs(ALERT_DELETE_ARGS, locations = ['query'])
    def delete(self, clear_until):
        check_alarm_setter()
        # Find current configuration
        current_config = Configuration.query.filter_by(current = True).first_or_404()
        # Build query based on passed arguments
        query = Alert.query.filter_by(config_id = current_config.id)
        if clear_until:
            query = query.filter(Alert.when <= clear_until)
        query.delete(synchronize_session = False)
        db.session.commit()
        return {}, 204

class MonitorDevicesResource(Resource):
    DEVICE_FIELDS = {
        'id': fields.Integer,
        'voltage_threshold': fields.Float,
        'latest_voltage': fields.Float,
        'latest_ping': fields.DateTime(dt_format = 'iso8601'),
        'time_since_latest_ping': fields.Integer,
        'voltage_alert': CodeToLabelField(ALERT_LEVELS),
        'ping_alert': CodeToLabelField(ALERT_LEVELS),
    }
    
    @marshal_with(DEVICE_FIELDS)
    def get(self):
        # Get list of all devices in current configuration and prepare for return to UI
        now = time()
        return [self._create_device_for_refresh(device, now) for device in MonitoringManager.instance.get_devices().values()]

    def _create_device_for_refresh(self, device, now):
        return {
            'id': device.source.device_id,
            'voltage_threshold': device.source.voltage_threshold,
            'latest_voltage': device.latest_voltage_level,
            'latest_ping': datetime.fromtimestamp(device.latest_ping),
            'time_since_latest_ping': now - device.latest_ping,
            'voltage_alert': device.latest_voltage_alert_level,
            'ping_alert': device.latest_ping_alert_level
        }
