# encoding: utf-8

from ... import db

from flask_restful import abort, fields, marshal_with, Resource
from flask_restful.fields import Raw
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs

from app.models import Account
from app.common import trim

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

class UsersResource(Resource):
    USER_ARGS = {
        'username': Arg(str, required = True, use = trim),
        'fullname': Arg(str, required = True, use = trim),
        'password': Arg(str, required = True),
        'role': Arg(int, required = True, use = role)
    }
    
    @marshal_with(USER_FIELDS)
    def get(self):
        return Account.query.all()

    @use_kwargs(USER_ARGS, locations = ['json'])
    @marshal_with(USER_FIELDS)
    def post(self, **args):
        #TODO optimize and avoid creating the object; checking it exists is enough!
        if Account.query.filter_by(username = args['username']).first():
            abort(409, message = {'username': 'A user already exists with that name!'})
        account = Account(**args)
        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)
        return account, 201

class UserResource(Resource):
    USER_ARGS = {
        'username': Arg(str, required = False, use = trim, allow_missing = True),
        'fullname': Arg(str, required = False, use = trim, allow_missing = True),
        'password': Arg(str, required = False, allow_missing = True),
        'role': Arg(int, required = False, use = role, allow_missing = True)
    }
    
    @marshal_with(USER_FIELDS)
    def get(self, id):
        return Account.query.get_or_404(id)

    def delete(self, id):
        account = Account.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        return {}, 204

    @use_args(USER_ARGS, locations = ['json'])
    @marshal_with(USER_FIELDS)
    def put(self, args, id):
        account = Account.query.get_or_404(id)
        for key, value in args.items():
            setattr(account, key, value)
        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)
        return account, 200
    