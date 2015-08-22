# encoding: utf-8

from ... import db
from ...models import Device

from flask_restful import abort, fields, marshal_with, reqparse, Resource
from flask_restful.fields import Raw

KINDS = [
    (Device.KIND_KEYPAD, 'Keypad'),
    (Device.KIND_MOTION, 'Motion'),
    (Device.KIND_CAMERA, 'Camera'),
]
    
class Kind(Raw):
    def format(self, value):
        for (code, label) in KINDS:
            if value == code:
                return label
        return None

def kind(value):
    for (code, label) in KINDS:
        if value == label:
            return code
    return None

DEVICE_FIELDS = {
    'id': fields.Integer,
    'name': fields.String,
    'kind': Kind,
    'device_id': fields.Integer,
    'voltage_threshold': fields.Float,
    'location_x': fields.Float,
    'location_y': fields.Float,
    'uri': fields.Url('.device', absolute =  False)
}

class DevicesResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        self.reqparse.add_argument(
            'name', required = True, type = str, location = 'json', trim = True)
        self.reqparse.add_argument(
            'kind', required = True, type = kind, location = 'json')
        self.reqparse.add_argument(
            'device_id', required = True, type = int, location = 'json')
        self.reqparse.add_argument(
            'voltage_threshold', required = True, type = float, location = 'json')
        self.reqparse.add_argument(
            'location_x', required = False, type = float, location = 'json')
        self.reqparse.add_argument(
            'location_y', required = False, type = float, location = 'json')
    
    @marshal_with(DEVICE_FIELDS)
    def get(self, id):
        return Device.query.filter_by(config_id = id).all()

    @marshal_with(DEVICE_FIELDS)
    def post(self, id):
        args = self.reqparse.parse_args(strict = True)
        #TODO optimize and avoid creating the object; checking it exists is enough!
        if Device.query.filter_by(config_id = id, device_id = args.device_id).first():
            abort(409, message = {'device_id': 'A device already exists with that device ID!'})
        if Device.query.filter_by(config_id = id, name = args.name).first():
            abort(409, message = {'device_name': 'A device already exists with that name!'})
        device = Device(**args)
        device.config_id = id
        db.session.add(device)
        db.session.commit()
        db.session.refresh(device)
        return device, 201

class DeviceResource(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        self.reqparse.add_argument(
            'name', required = False, type = str, location = 'json', store_missing = False, trim = True)
        self.reqparse.add_argument(
            'kind', required = False, type = kind, location = 'json', store_missing = False)
        self.reqparse.add_argument(
            'device_id', required = False, type = int, location = 'json', store_missing = False)
        self.reqparse.add_argument(
            'voltage_threshold', required = False, type = float, location = 'json', store_missing = False)
        self.reqparse.add_argument(
            'location_x', required = False, type = float, location = 'json', store_missing = False)
        self.reqparse.add_argument(
            'location_y', required = False, type = float, location = 'json', store_missing = False)

    @marshal_with(DEVICE_FIELDS)
    def get(self, id):
        return Device.query.get_or_404(id)

    def delete(self, id):
        device = Device.query.get_or_404(id)
        db.session.delete(device)
        db.session.commit()
        return {}, 204

    @marshal_with(DEVICE_FIELDS)
    def put(self, id):
        device = Device.query.get_or_404(id)
        args = self.reqparse.parse_args(strict = True)
        for key, value in args.items():
            setattr(device, key, value)
        db.session.add(device)
        db.session.commit()
        db.session.refresh(device)
        return device, 200
