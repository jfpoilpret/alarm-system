# encoding: utf-8

from ... import db

from flask_restful import fields, marshal_with, Resource

from webargs import Arg
from webargs.flaskparser import use_args

from app.models import Alert, Configuration, NoPingTimeAlertThreshold, VoltageRateAlertThreshold
from app.common import check_configurator

ALERT_LEVELS = [
    (Alert.LEVEL_INFO, 'info'),
    (Alert.LEVEL_WARNING, 'warning'),
    (Alert.LEVEL_ALARM, 'alarm'),
]
    
NO_PING_ALERT_THRESHOLD_FIELDS = {}
NO_PING_ALERT_THRESHOLD_ARGS = {}
for _, level in ALERT_LEVELS:
    NO_PING_ALERT_THRESHOLD_FIELDS[level] = fields.List(fields.Integer)
    NO_PING_ALERT_THRESHOLD_ARGS[level] = Arg(int, required = True, multiple = True)

class NoPingAlertThresholdsResource(Resource):
    @marshal_with(NO_PING_ALERT_THRESHOLD_FIELDS)
    def get(self, id):
        check_configurator()
        config = Configuration.query.get_or_404(id)
        return self.convert_thresholds(config), 200

    @use_args(NO_PING_ALERT_THRESHOLD_ARGS, locations = ['json'])
    @marshal_with(NO_PING_ALERT_THRESHOLD_FIELDS)
    def put(self, args, id):
        check_configurator()
        config = Configuration.query.get_or_404(id)
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
        check_configurator()
        config = Configuration.query.get_or_404(id)
        return self.convert_thresholds(config), 200

    @use_args(VOLTAGE_ALERT_THRESHOLD_ARGS, locations = ['json'])
    @marshal_with(VOLTAGE_ALERT_THRESHOLD_FIELDS)
    def put(self, args, id):
        check_configurator()
        config = Configuration.query.get_or_404(id)
        config.voltage_rate_alert_thresholds = []
        for level, label in ALERT_LEVELS:
            for threshold in args[label]:
                threshold = VoltageRateAlertThreshold(
                    alert_level = level,
                    alert_time = threshold['time'],
                    voltage_rate = threshold['rate'])
                config.voltage_rate_alert_thresholds.append(threshold)
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return self.convert_thresholds(config), 200

    def convert_thresholds(self, config):
        all_thresholds = config.voltage_rate_alert_thresholds
        thresholds = {}
        for level, label in ALERT_LEVELS:
            values = [{'rate': threshold.voltage_rate, 'time': threshold.alert_time}
                for threshold in all_thresholds if threshold.alert_level == level]
            thresholds[label] = sorted(values, key = lambda t: t['rate'], reverse = True)
        return thresholds
    