# encoding: utf-8

from ... import db

from flask import request
from flask_restful import abort, fields, marshal_with, reqparse, Resource
from flask_restful.fields import Raw

from webargs import Arg
from webargs.flaskparser import parser, use_kwargs

from app.models import Alert, NoPingTimeAlertThreshold, Configuration

ALERT_LEVELS = [
    (Alert.LEVEL_INFO, 'info'),
    (Alert.LEVEL_WARNING, 'warning'),
    (Alert.LEVEL_ALARM, 'alarm'),
]
    
NO_PING_ALERT_THRESHOLD_FIELDS = {}
for _, level in ALERT_LEVELS:
    NO_PING_ALERT_THRESHOLD_FIELDS[level] = fields.List(fields.Integer)

class NoPingAlertThresholdsResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        for _, label in ALERT_LEVELS:
            self.reqparse.add_argument(label, required = True, type = list, location = 'json')
    
    @marshal_with(NO_PING_ALERT_THRESHOLD_FIELDS)
    def get(self, id):
        config = Configuration.query.get_or_404(id)
        return self.convert_thresholds(config), 200

    @marshal_with(NO_PING_ALERT_THRESHOLD_FIELDS)
    def put(self, id):
        config = Configuration.query.get_or_404(id)
        args = self.reqparse.parse_args(strict = True)
        config.no_ping_time_alert_thresholds = []
        for level, label in ALERT_LEVELS:
            for time in args[label]:
                threshold = NoPingTimeAlertThreshold(
                    alert_level = level,
                    alert_time = time)
                config.no_ping_time_alert_thresholds.append(threshold)
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return self.convert_thresholds(config), 200

    def convert_thresholds(self, config):
        all_thresholds = config.no_ping_time_alert_thresholds
        thresholds = {}
        for level, label in ALERT_LEVELS:
            times = [threshold.alert_time for threshold in all_thresholds if threshold.alert_level == level]
            thresholds[label] = sorted(times)
        return thresholds

VOLTAGE_THRESHOLD_FIELDS = {
    'rate': fields.Integer,
    'time': fields.Integer
}
VOLTAGE_THRESHOLD_ARGS = {
    'rate': Arg(int, required = True),
    'time': Arg(int, required = True)
}

VOLTAGE_ALERT_THRESHOLD_FIELDS = {}
VOLTAGE_ALERT_THRESHOLD_ARGS = {}
for _, level in ALERT_LEVELS:
    VOLTAGE_ALERT_THRESHOLD_FIELDS[level] = fields.List(fields.Nested(VOLTAGE_THRESHOLD_FIELDS))
    VOLTAGE_ALERT_THRESHOLD_ARGS[level] = Arg(VOLTAGE_THRESHOLD_ARGS, required = True, multiple = True)

class VoltageAlertThresholdsResource(Resource):
    @marshal_with(VOLTAGE_ALERT_THRESHOLD_FIELDS)
    def get(self, id):
        config = Configuration.query.get_or_404(id)
        return self.convert_thresholds(config), 200

    @marshal_with(VOLTAGE_ALERT_THRESHOLD_FIELDS)
    @use_kwargs(VOLTAGE_ALERT_THRESHOLD_ARGS, locations = ['json'])
    def put(self, id, info, warning, alarm):
        print('put(%d) info = %s' % (id, str(info)))
        print('put(%d) warning = %s' % (id, str(warning)))
        print('put(%d) alarm = %s' % (id, str(alarm)))
        config = Configuration.query.get_or_404(id)
        return self.convert_thresholds(config), 200

    def convert_thresholds(self, config):
        all_thresholds = config.voltage_rate_alert_thresholds
        thresholds = {}
        for level, label in ALERT_LEVELS:
            values = [{'rate': threshold.voltage_rate, 'time': threshold.alert_time}
                for threshold in all_thresholds if threshold.alert_level == level]
            thresholds[label] = sorted(values, key = 'rate', reverse = True)
        return thresholds
    