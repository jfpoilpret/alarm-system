# encoding: utf-8

from ... import db

from flask_restful import abort, fields, marshal_with, Resource
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs
from sqlalchemy import update

from app.models import Configuration, Alert, AlertType
from app.common import trim, choices, CodeToLabelField, label_to_code
from app.monitor.monitoring import AlarmStatus, MonitoringManager
from flask_restful.fields import Raw
from datetime import date

#TODO resources to GET:
# - status: GET/PUT (active/lock)
#     return jsonify(
#         active = active, 
#         locked = locked, 
#         status = status_display, 
#         hashcode = status_hash_code,
#         namehash = config_name_hash_code)
#
# - alerts GET/DELETE
#    with query args (history search or update realtime alerts)
#
# - devices status GET
#    

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
        return self.get_status(config)

    @use_kwargs(CONFIG_ARGS, locations = ['json'])
    @marshal_with(CONFIG_FIELDS)
    def put(self, active, locked):
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
            currently_locked = (MonitoringManager.instance.get_status() == AlarmStatus.LOCKED)
            if locked is not None and locked != currently_locked:
                if locked:
                    MonitoringManager.instance.lock()
                else:
                    MonitoringManager.instance.unlock()
        return self.get_status(config)

    def get_status(self, config):
        locked = (MonitoringManager.instance.get_status() == AlarmStatus.LOCKED)
        return {
            'id': config.id,
            'name': config.name,
            'active': config.active, 
            'locked': locked
        }

ALERT_LEVELS = [
    (Alert.LEVEL_INFO, 'info'),
    (Alert.LEVEL_WARNING, 'warning'),
    (Alert.LEVEL_ALARM, 'alarm'),
]

class AlertLevelField(Raw):
    def format(self, value):
        for (code, label) in ALERT_LEVELS:
            if value == code:
                return label
        return None

ALERT_TYPES = [
    (AlertType.DEVICE_NO_PING_FOR_TOO_LONG, 'no-ping'),
    (AlertType.DEVICE_VOLTAGE_UNDER_THRESHOLD, 'voltage-level'),
    (AlertType.LOCK, 'lock'),
    (AlertType.UNLOCK, 'unlock'),
    (AlertType.SYSTEM_ACTIVATION, 'activation'),
    (AlertType.SYSTEM_DEACTIVATION, 'deactivation'),
    (AlertType.WRONG_LOCK_CODE, 'wrong-code'),
]

class AlertTypeField(Raw):
    def format(self, value):
        for (code, label) in ALERT_TYPES:
            if value == code:
                return label
        return None

class MonitorAlertsResource(Resource):
    #TODO nested field for device
    ALERT_FIELDS = {
        'id': fields.Integer,
        'when': fields.DateTime(),
#         'level': AlertLevelField,
#         'alert_type': AlertTypeField,
        'level': CodeToLabelField(ALERT_LEVELS),
        'alert_type': CodeToLabelField(ALERT_TYPES),
        'message': fields.String,
    }

    #TODO allow multiple alert levels and types
    ALERT_GET_ARGS = {
        'since_id': Arg(int, required = False),
        'max_count': Arg(int, required = False, default = 100),
        'period_from': Arg(date, required = False),
        'period_to': Arg(date, required = False),
        'alert_level': Arg(int, required = False, use = label_to_code(ALERT_LEVELS)),
        'alert_type': Arg(int, required = False, use = label_to_code(ALERT_TYPES)),
    }
    #TODO make since_id exclusive with all other fields with validate = xxx
    @use_args(ALERT_GET_ARGS, locations = ['query'])
    @marshal_with(ALERT_FIELDS)
    def get(self, args):
        # Find current configuration
        current_config = Configuration.query.filter_by(current = True).first_or_404()
        # Build query based on passed arguments
        query = Alert.query.filter_by(config_id = current_config.id)
        if args.has_key('since_id'):
            query = query.filter(Alert.id > args['since_id'])
        if args.has_key('period_from'):
            query = query.filter(Alert.when >= args['period_from'])
        if args.has_key('period_to'):
            query = query.filter(Alert.when <= args['period_to'])
        if args.has_key('alert_level'):
            query = query.filter_by(level = args['alert_level'])
        if args.has_key('alert_type'):
            query = query.filter_by(alert_type = args['alert_type'])
        # Limit number of retrieved records
        query = query.order_by(Alert.when.desc())
        if args.has_key('max_count') and args['max_count']:
            query = query.limit(args['max_count'])
        return query.all()
    
    #TODO allow more filters: levels/types of alerts
    ALERT_DELETE_ARGS = {
        'clear_until': Arg(date, required = False),
    }

    @use_kwargs(ALERT_DELETE_ARGS, locations = ['query'])
    def delete(self, clear_until):
        #TODO
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
    pass
