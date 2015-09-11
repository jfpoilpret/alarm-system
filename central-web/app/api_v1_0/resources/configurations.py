# encoding: utf-8

from ... import db

from flask_restful import abort, fields, marshal_with, Resource
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs
from sqlalchemy import update

from app.models import Alert, Configuration, NoPingTimeAlertThreshold, VoltageRateAlertThreshold
from app.common import prepare_map_for_config, prepare_map_for_monitoring, trim, choices

CONFIG_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'current': fields.Boolean,
    'active': fields.Boolean,
    'lockcode': fields.String,
    'map_area_filename': fields.String,
    'uri': fields.Url('.configuration', absolute =  False),
    'map': fields.Url('.map', absolute =  False),
    'devices': fields.Url('.devices', absolute = False),
    'no_ping_thresholds': fields.Url('.no-ping', absolute = False),
    'voltage_thresholds': fields.Url('.voltage', absolute = False)
}

class ConfigurationsResource(Resource):
    CONFIG_ARGS = {
        'name': Arg(str, required = True, use = trim),
        'lockcode': Arg(str, required = True, use = trim)
    }
    
    @marshal_with(CONFIG_FIELDS)
    def get(self):
        return Configuration.query.all()

    @use_kwargs(CONFIG_ARGS, locations = ['json'])
    @marshal_with(CONFIG_FIELDS)
    def post(self, **args):
        #TODO optimize and avoid creating the object; checking it exists is enough!
        if Configuration.query.filter_by(name = args['name']).first():
            abort(409, message = {'name': 'A configuration already exists with that name!'})
        configuration = Configuration(**args)
        configuration.active = False
        configuration.current = False
        # Add default alert thresholds
        self.init_new_config(configuration)
        db.session.add(configuration)
        db.session.commit()
        db.session.refresh(configuration)
        return configuration, 201

    def init_new_config(self, config):
        config.no_ping_time_alert_thresholds = [
            NoPingTimeAlertThreshold(alert_time = 10, alert_level = Alert.LEVEL_INFO),
            NoPingTimeAlertThreshold(alert_time = 20, alert_level = Alert.LEVEL_WARNING),
            NoPingTimeAlertThreshold(alert_time = 60, alert_level = Alert.LEVEL_ALARM),
        ]
        config.voltage_rate_alert_thresholds = [
            VoltageRateAlertThreshold(voltage_rate = 100.0, alert_level = Alert.LEVEL_INFO, alert_time = 60),
            VoltageRateAlertThreshold(voltage_rate = 90.0, alert_level = Alert.LEVEL_WARNING, alert_time = 30),
            VoltageRateAlertThreshold(voltage_rate = 80.0, alert_level = Alert.LEVEL_ALARM, alert_time = 10),
        ]


class ConfigurationResource(Resource):
    CONFIG_ARGS = {
        'name': Arg(str, required = False, allow_missing = True, use = trim),
        'lockcode': Arg(str, required = False, allow_missing = True, use = trim)
    }
    
    @marshal_with(CONFIG_FIELDS)
    def get(self, id):
        return Configuration.query.get_or_404(id)

    def delete(self, id):
        config = Configuration.query.get_or_404(id)
        db.session.delete(config)
        db.session.commit()
        return {}, 204

    @use_args(CONFIG_ARGS, locations = ['json'])
    @marshal_with(CONFIG_FIELDS)
    def put(self, args, id):
        config = Configuration.query.get_or_404(id)
        for key, value in args.items():
            setattr(config, key, value)
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config, 200

#TODO remove prepare_for=monitoring
class ConfigurationMapResource(Resource):
    @use_kwargs({ 'prepare_for': Arg(str, required = False, location = 'query', 
                    validate = choices('configuration', 'monitoring')) })
    def get(self, id, prepare_for):
        config = Configuration.query.get_or_404(id)
        if prepare_for == 'configuration':
            return prepare_map_for_config(config)
        elif prepare_for == 'monitoring':
            return prepare_map_for_monitoring(config)
        else:
            return config.map_area

    @marshal_with(CONFIG_FIELDS)
    def delete(self, id):
        config = Configuration.query.get_or_404(id)
        config.map_area = None
        config.map_area_filename = None
        db.session.commit()
        db.session.refresh(config)
        return config, 200

    @use_kwargs({ 'map_area': Arg(required = True, location = 'files') })
    @marshal_with(CONFIG_FIELDS)
    def post(self, id, map_area):
        config = Configuration.query.get_or_404(id)
        data = map_area.read().decode('utf-8')
        config.map_area = data
        config.map_area_filename = map_area.filename
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config, 200

class CurrentConfigurationResource(Resource):
    @marshal_with(CONFIG_FIELDS)
    def get(self):
        config = Configuration.query.filter_by(current = True).first()
        if config:
            return config, 200
        else:
            return {}, 204
    
    @use_kwargs({ 'id': Arg(int, required = True, location = 'query') })
    @marshal_with(CONFIG_FIELDS)
    def post(self, id):
        config = Configuration.query.get_or_404(id)
        if not config.current:
            db.session.execute(update(Configuration.__table__).values(current = False))
            config.current = True
            db.session.add(config)
            db.session.commit()
            db.session.refresh(config)
            return config, 200
        else:
            return {}, 204
