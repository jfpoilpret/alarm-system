# encoding: utf-8

from ... import db

from flask import url_for
from flask_restful import abort, fields, marshal_with, Resource
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs
from sqlalchemy import update

from app.models import Alert, Configuration, NoPingTimeAlertThreshold, VoltageRateAlertThreshold
from app.common import trim, choices, check_configurator, prepare_map
from xmltodict import parse, unparse

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
        check_configurator()
        return Configuration.query.all()

    @use_kwargs(CONFIG_ARGS, locations = ['json'])
    @marshal_with(CONFIG_FIELDS)
    def post(self, **args):
        check_configurator()
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
        check_configurator()
        return Configuration.query.get_or_404(id)

    def delete(self, id):
        check_configurator()
        config = Configuration.query.get_or_404(id)
        db.session.delete(config)
        db.session.commit()
        return {}, 204

    @use_args(CONFIG_ARGS, locations = ['json'])
    @marshal_with(CONFIG_FIELDS)
    def put(self, args, id):
        check_configurator()
        config = Configuration.query.get_or_404(id)
        for key, value in args.items():
            setattr(config, key, value)
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config, 200

class ConfigurationMapResource(Resource):
    @use_kwargs({ 'prepare_for': Arg(str, required = False, location = 'query', 
                    validate = choices('configuration')) })
    def get(self, id, prepare_for):
        check_configurator()
        config = Configuration.query.get_or_404(id)
        if prepare_for == 'configuration':
            return self.prepare_map_for_config(config)
        else:
            return config.map_area

    @marshal_with(CONFIG_FIELDS)
    def delete(self, id):
        check_configurator()
        config = Configuration.query.get_or_404(id)
        config.map_area = None
        config.map_area_filename = None
        db.session.commit()
        db.session.refresh(config)
        return config, 200

    @use_kwargs({ 'map_area': Arg(required = True, location = 'files') })
    @marshal_with(CONFIG_FIELDS)
    def post(self, id, map_area):
        check_configurator()
        config = Configuration.query.get_or_404(id)
        data = map_area.read().decode('utf-8')
        config.map_area = data
        config.map_area_filename = map_area.filename
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config, 200

    # This function reads an SVG string (XML) containing the monitoring zone map,
    # adds a layer for devices, and prepares the result for direct SVG embedding to HTML
    def prepare_map_for_config(self, config):
        def update_image(device_image):
            device_image['@onmousedown'] = 'svg.startDrag(evt)'
            device_image['@onmousemove'] = 'svg.drag(evt)'
            device_image['@onmouseup'] = 'svg.endDrag(evt)'
        def update_group(device_group):
            device_group['@class'] = 'device-image'
        svg_xml = parse(config.map_area, process_namespaces = False)
        dimensions = prepare_map(svg_xml)
        self.prepare_devices(config.devices, svg_xml['svg']['g'], dimensions, update_image, update_group)
        return unparse(svg_xml, full_document = False)
    
    def prepare_devices(self, devices, layers, dimensions, update_device_image, update_device_group):
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
                    '@data-uri': url_for('.device', id = device.id),
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
    
class CurrentConfigurationResource(Resource):
    @marshal_with(CONFIG_FIELDS)
    def get(self):
        check_configurator()
        config = Configuration.query.filter_by(current = True).first()
        if config:
            return config, 200
        else:
            return {}, 204
    
    @use_kwargs({ 'id': Arg(int, required = True, location = 'query') })
    @marshal_with(CONFIG_FIELDS)
    def post(self, id):
        check_configurator()
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
