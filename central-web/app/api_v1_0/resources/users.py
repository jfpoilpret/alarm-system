# encoding: utf-8

from ... import db

from flask import g
from flask_restful import abort, fields, marshal_with, Resource
from webargs import Arg
from webargs.flaskparser import use_args, use_kwargs

from app.models import Account
from app.common import trim, check_admin, CodeToLabelField, ROLES, label_to_code

USER_FIELDS = {
    'id': fields.Integer,
    'username': fields.String,
    'fullname': fields.String,
    'role': CodeToLabelField(ROLES),
    'uri': fields.Url('.user', absolute =  False)
}

class UsersResource(Resource):
    USER_ARGS = {
        'username': Arg(str, required = True, use = trim),
        'fullname': Arg(str, required = True, use = trim),
        'password': Arg(str, required = True),
        'role': Arg(int, required = True, use = label_to_code(ROLES))
    }
    
    @marshal_with(USER_FIELDS)
    def get(self):
        check_admin()
        return Account.query.all()

    @use_kwargs(USER_ARGS, locations = ['json'])
    @marshal_with(USER_FIELDS)
    def post(self, **args):
        check_admin()
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
        'role': Arg(int, required = False, use = label_to_code(ROLES), allow_missing = True)
    }
    
    @marshal_with(USER_FIELDS)
    def get(self, id):
        if g.user.id != id:
            check_admin()
        return Account.query.get_or_404(id)

    def delete(self, id):
        check_admin()
        account = Account.query.get_or_404(id)
        db.session.delete(account)
        db.session.commit()
        return {}, 204

    @use_args(USER_ARGS, locations = ['json'])
    @marshal_with(USER_FIELDS)
    def put(self, args, id):
        if g.user.id != id:
            check_admin()
        account = Account.query.get_or_404(id)
        for key, value in args.items():
            setattr(account, key, value)
        db.session.add(account)
        db.session.commit()
        db.session.refresh(account)
        return account, 200
    