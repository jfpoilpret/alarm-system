# encoding: utf-8

from ... import db

from flask_restful import fields, marshal_with, Resource
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs

from app.models import Configuration, Alert, AlertType, Device
from app.common import CodeToLabelField, string_to_date, check_alarm_setter

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

class IterPage(fields.Raw):
    def output(self, key, obj):
        return list(obj.iter_pages(left_edge = 1, right_edge = 1, left_current = 2, right_current = 3))

class AlertsHistoryResource(Resource):
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
    
    PAGE_FIELDS = {
        'alerts': fields.List(fields.Nested(ALERT_FIELDS), attribute = 'items'),
        'total': fields.Integer,
        'page': fields.Integer,
        'pages': fields.Integer,
        'has_prev': fields.Boolean,
        'has_next': fields.Boolean,
        'prev_num': fields.Integer,
        'next_num': fields.Integer,
        'iter_pages': IterPage
    }

    ALERT_GET_ARGS = {
        'per_page': Arg(int, required = False, default = 20, allow_missing = True),
        'page': Arg(int, required = False, default = 1, allow_missing = True)
    }

    @use_args(ALERT_GET_ARGS, locations = ['query'])
    @marshal_with(PAGE_FIELDS)
    def get(self, args, id):
        # Check requested configuration exists
        Configuration.query.get_or_404(id)
        # Build query based on passed arguments
        query = Alert.query.filter_by(config_id = id).order_by(Alert.id.desc())
        return query.paginate(args['page'], args['per_page'])
    
    #TODO allow more filters: levels/types of alerts
    ALERT_DELETE_ARGS = {
        'clear_until': Arg(required = False, use = string_to_date()),
    }

    @use_kwargs(ALERT_DELETE_ARGS, locations = ['query'])
    def delete(self, id, clear_until):
        check_alarm_setter()
        # Check requested configuration exists
        Configuration.query.get_or_404(id)
        # Build query based on passed arguments
        query = Alert.query.filter_by(config_id = id)
        if clear_until:
            query = query.filter(Alert.when <= clear_until)
        query.delete(synchronize_session = False)
        db.session.commit()
        return {}, 204
