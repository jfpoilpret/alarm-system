# encoding: utf-8

from ... import db
from app.models import Device, Configuration

from flask_restful import abort, fields, marshal_with, Resource
from flask_restful.fields import Raw
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs
from app.common import trim, extract_viewbox_from_config, check_configurator,\
    CodeToLabelField, label_to_code

KINDS = [
    (Device.KIND_KEYPAD, 'Keypad'),
    (Device.KIND_MOTION, 'Motion'),
    (Device.KIND_CAMERA, 'Camera'),
]
    
DEVICE_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'kind': CodeToLabelField(KINDS),
    'device_id': fields.Integer,
    'voltage_threshold': fields.Float,
    'location_x': fields.Float,
    'location_y': fields.Float,
    'uri': fields.Url('.device', absolute =  False)
}

class DevicesResource(Resource):
    DEVICE_ARGS = {
        'name': Arg(str, required = True,  use = trim),
        'kind': Arg(int, required = True,  use = label_to_code(KINDS)),
        'device_id': Arg(int, required = True),
        'voltage_threshold': Arg(float, required = True),
        'location_x': Arg(float, required = False, allow_missing = True),
        'location_y': Arg(float, required = False, allow_missing = True)
    }
    
    @marshal_with(DEVICE_FIELDS)
    def get(self, id):
        check_configurator()
        return Device.query.filter_by(config_id = id).all()

    @use_kwargs(DEVICE_ARGS, locations = ['json'])
    @marshal_with(DEVICE_FIELDS)
    def post(self, id, **args):
        check_configurator()
        #TODO optimize and avoid creating the object; checking it exists is enough!
        if Device.query.filter_by(config_id = id, device_id = args['device_id']).first():
            abort(409, message = {'device_id': 'A device already exists with that device ID!'})
        if Device.query.filter_by(config_id = id, name = args['name']).first():
            abort(409, message = {'device_name': 'A device already exists with that name!'})
        device = Device(**args)
        device.config_id = id
        db.session.add(device)
        db.session.commit()
        db.session.refresh(device)
        return device, 201

class DeviceResource(Resource):
    #TODO Add validation of kind Vs. device_id
    DEVICE_ARGS = {
        'name': Arg(str, required = False,  use = trim, allow_missing = True),
        'kind': Arg(int, required = False,  use = label_to_code(KINDS), allow_missing = True),
        'device_id': Arg(int, required = False, allow_missing = True),
        'voltage_threshold': Arg(float, required = False, allow_missing = True),
        'location_x': Arg(float, required = False, allow_missing = True),
        'location_y': Arg(float, required = False, allow_missing = True)
    }
    
    @marshal_with(DEVICE_FIELDS)
    def get(self, id):
        check_configurator()
        return Device.query.get_or_404(id)

    def delete(self, id):
        check_configurator()
        device = Device.query.get_or_404(id)
        db.session.delete(device)
        db.session.commit()
        return {}, 204

    @use_args(DEVICE_ARGS, locations = ['json'])
    @marshal_with(DEVICE_FIELDS)
    def put(self, args, id):
        check_configurator()
        device = Device.query.get_or_404(id)
        config = Configuration.query.get_or_404(device.config_id)
        x = args.get('location_x', None)
        y = args.get('location_y', None)
        if x is not None or y is not None:
            # Normalize locations if needed
            dimensions = extract_viewbox_from_config(config)
            # interpret all devices locations (as ratios)
            if x is not None:
                args['location_x'] = (x - dimensions[0]) / dimensions[2]
            if y is not None:
                args['location_y'] = (y - dimensions[1]) / dimensions[3]
        for key, value in args.items():
            setattr(device, key, value)
        db.session.add(device)
        db.session.add(device)
        db.session.commit()
        db.session.refresh(device)
        return device, 200
