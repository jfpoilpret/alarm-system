# encoding: utf-8

from ... import db

from flask_restful import abort, fields, marshal_with, reqparse, Resource
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs
from werkzeug.datastructures import FileStorage
from sqlalchemy import update

from app.models import Configuration
from app.common import prepare_map_for_config, prepare_map_for_monitoring, trim

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

#FIXME should remove map_are from settable fields!
class ConfigurationsResource(Resource):
    CONFIG_ARGS = {
        'name': Arg(str, required = True, use = trim),
        'lockcode': Arg(str, required = True, use = trim),
        'map_area_filename': Arg(str, required = False, allow_missing = True, use = trim),
        'map_area': Arg(str, required = False, allow_missing = True, use = trim)
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
        db.session.add(configuration)
        db.session.commit()
        #TODO Add default alert thresholds
        db.session.refresh(configuration)
        return configuration, 201

#FIXME should remove current (active also?) from settable fields!
class ConfigurationResource(Resource):
    CONFIG_ARGS = {
        'name': Arg(str, required = False, allow_missing = True, use = trim),
        'lockcode': Arg(str, required = False, allow_missing = True, use = trim),
        'current': Arg(bool, required = False, allow_missing = True),
        'active': Arg(str, required = False, allow_missing = True)
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

class ConfigurationMapResource(Resource):
    def __init__(self):
        self.get_parse = reqparse.RequestParser(bundle_errors = True)
        self.get_parse.add_argument(
            'prepare_for', required = False, type = str, location = 'args', 
            choices = ['configuration', 'monitoring'])
        self.post_parse = reqparse.RequestParser(bundle_errors = True)
        self.post_parse.add_argument(
            'map_area', required = True, type = FileStorage, location = 'files')

    def get(self, id):
        config = Configuration.query.get_or_404(id)
        args = self.get_parse.parse_args(strict = True)
        if args.prepare_for == 'configuration':
            return prepare_map_for_config(config)
        elif args.prepare_for == 'monitoring':
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

    @marshal_with(CONFIG_FIELDS)
    def post(self, id):
        config = Configuration.query.get_or_404(id)
        args = self.post_parse.parse_args(strict = True)
        data = args.map_area.read().decode('utf-8')
        config.map_area = data
        config.map_area_filename = args.map_area.filename
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config, 200

class CurrentConfigurationResource(Resource):
    def __init__(self):
        self.post_parse = reqparse.RequestParser(bundle_errors = True)
        self.post_parse.add_argument(
            'id', required = True, type = int, location = 'args')
    
    @marshal_with(CONFIG_FIELDS)
    def get(self):
        config = Configuration.query.filter_by(current = True).first()
        if config:
            return config, 200
        else:
            return {}, 204
    
    @marshal_with(CONFIG_FIELDS)
    def post(self):
        args = self.post_parse.parse_args(strict = True)
        config = Configuration.query.get_or_404(args.id)
        if not config.current:
            db.session.execute(update(Configuration.__table__).values(current = False))
            config.current = True
            db.session.add(config)
            db.session.commit()
            db.session.refresh(config)
            return config, 200
        else:
            return {}, 204
