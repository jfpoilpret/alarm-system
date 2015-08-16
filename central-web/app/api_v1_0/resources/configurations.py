# encoding: utf-8

from ... import db
from ...models import Configuration

from flask_restful import abort, fields, marshal_with, reqparse, Resource
from werkzeug.datastructures import FileStorage

CONFIG_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'current': fields.Boolean,
    'active': fields.Boolean,
    'lockcode': fields.String,
    'map_area_filename': fields.String,
    'uri': fields.Url('.configuration', absolute =  False),
    'map': fields.Url('.map', absolute =  False)
    #TODO Add uri to get devices, no_ping_time_alert_thresholds, voltage_rate_alert_thresholds
}

class ConfigurationsResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        self.reqparse.add_argument(
            'name', required = True, type = str, location = 'json', trim = True)
        self.reqparse.add_argument(
            'lockcode', required = True, type = str, location = 'json', trim = True)
        self.reqparse.add_argument(
            'map_area_filename', required = False, type = str, location = 'json', trim = True)
        self.reqparse.add_argument(
            'map_area', required = False, type = str, location = 'json', trim = True)
    
    @marshal_with(CONFIG_FIELDS)
    def get(self):
        return Configuration.query.all()

    @marshal_with(CONFIG_FIELDS)
    def post(self):
        args = self.reqparse.parse_args(strict = True)
        #TODO optimize and avoid creating the object; checking it exists is enough!
        if Configuration.query.filter_by(name = args.name).first():
            abort(409, message = {'name': 'A configuration already exists with that name!'})
        configuration = Configuration(**args)
        configuration.active = False
        configuration.current = False
        db.session.add(configuration)
        db.session.commit()
        #TODO Add default alert thresholds
        db.session.refresh(configuration)
        return configuration, 201

class ConfigurationResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        self.reqparse.add_argument(
            'name', required = False, type = str, location = 'json', store_missing = False, trim = True)
        self.reqparse.add_argument(
            'current', required = False, type = bool, location = 'json', store_missing = False)
        self.reqparse.add_argument(
            'active', required = False, type = bool, location = 'json', store_missing = False)
        self.reqparse.add_argument(
            'lockcode', required = False, type = str, location = 'json', store_missing = False, trim = True)

    @marshal_with(CONFIG_FIELDS)
    def get(self, id):
        return Configuration.query.get_or_404(id)

    def delete(self, id):
        config = Configuration.query.get_or_404(id)
        db.session.delete(config)
        db.session.commit()
        return {}, 204

    @marshal_with(CONFIG_FIELDS)
    def put(self, id):
        config = Configuration.query.get_or_404(id)
        args = self.reqparse.parse_args(strict = True)
        #TODO check current is set only if no config exists currently current
        #TODO check active is set only if config is current
        for key, value in args.items():
            setattr(config, key, value)
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config, 200

class ConfigurationMapResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        self.reqparse.add_argument(
            'map_area', required = True, type = FileStorage, location = 'files')

    def get(self, id):
        config = Configuration.query.get_or_404(id)
        #TODO Prepare map for config of devices?
        return config.map_area

    @marshal_with(CONFIG_FIELDS)
    def delete(self, id):
        config = Configuration.query.get_or_404(id)
        config.map_area = None
        config.map_area_filename = None
        db.session.commit()
        db.session.refresh(config)
        return config, 200

    @marshal_with(CONFIG_FIELDS)
    def post(self, id):
        config = Configuration.query.get_or_404(id)
        args = self.reqparse.parse_args(strict = True)
        data = args.map_area.read().decode('utf-8')
        config.map_area = data
        config.map_area_filename = args.map_area.filename
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config, 200

#TODO other resources for: config devices (GET all/POST/GET/DELETE/PUT)
#TODO other resources for: ping thresholds (GET all/PUT only?)
#TODO other resources for: voltage thresholds (GET all/PUT only?)
