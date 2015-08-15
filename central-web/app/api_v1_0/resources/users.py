# encoding: utf-8

from ... import db
from ...models import Account

from flask_restful import abort, fields, marshal_with, reqparse, Resource
from flask_restful.fields import Raw


#TODO factor this out somewhere? (used in forms too)
ROLES = [
    (Account.ROLE_ADMINISTRATOR, 'Administrator'),
    (Account.ROLE_CONFIGURATOR, 'Configurator'),
    (Account.ROLE_ALARM_SETTER, 'Alarm Setter'),
    (Account.ROLE_ALARM_VIEWER, 'Alarm Viewer'),
]
    
class Role(Raw):
    def format(self, value):
        for (code, label) in ROLES:
            if value == code:
                return label
        return None

def role(value):
    for (code, label) in ROLES:
        if value == label:
            return code
    return None

USER_FIELDS = {
    'id': fields.Integer,
    'username': fields.String,
    'fullname': fields.String,
    'role': Role,
    'uri': fields.Url('.user', absolute =  False)
}

class Users(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        self.reqparse.add_argument(
            'username', required = True, type = str, location = 'json', trim = True)
        self.reqparse.add_argument(
            'fullname', required = True, type = str, location = 'json', trim = True)
        self.reqparse.add_argument(
            'password', required = True, type = str, location = 'json')
        self.reqparse.add_argument(
            'role', required = True, type = role, location = 'json')
    
    @marshal_with(USER_FIELDS)
    def get(self):
        return Account.query.all()

    @marshal_with(USER_FIELDS)
    def post(self):
        args = self.reqparse.parse_args(strict = True)
        #TODO optimize and avoid creating the object; checking it exists is enough!
        if Account.query.filter_by(username = args.username).first():
            abort(409, message = {'username': 'A user already exists with that name!'})
        account = Account(**args)
        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)
        return account, 201

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors = True)
        self.reqparse.add_argument(
            'username', required = False, type = str, location = 'json', store_missing = False, trim = True)
        self.reqparse.add_argument(
            'fullname', required = False, type = str, location = 'json', store_missing = False, trim = True)
        self.reqparse.add_argument(
            'password', required = False, type = str, location = 'json', store_missing = False)
        self.reqparse.add_argument(
            'role', required = False, type = role, location = 'json', store_missing = False)

    @marshal_with(USER_FIELDS)
    def get(self, id):
        return Account.query.get_or_404(id)

    def delete(self, id):
        account = Account.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        return {}, 204

    @marshal_with(USER_FIELDS)
    def put(self, id):
        account = Account.query.get_or_404(id)
        args = self.reqparse.parse_args(strict = True)
        for key, value in args.items():
            setattr(account, key, value)
        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)
        return account, 200
    