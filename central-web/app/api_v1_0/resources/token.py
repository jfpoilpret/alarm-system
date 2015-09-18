# encoding: utf-8

from flask import g
from flask_restful import fields, marshal_with, Resource
from webargs import Arg
from webargs.flaskparser import use_kwargs

from app.common import boolean, CodeToLabelField, ROLES

class TokenResource(Resource):
    USER_FIELDS = {
        'id': fields.Integer,
        'username': fields.String,
        'fullname': fields.String,
        'role': CodeToLabelField(ROLES),
        'uri': fields.Url('.user', absolute =  False)
    }
    AUTH_FIELDS = {
        'token': fields.String,
        'renew_before': fields.Integer,
        'user': fields.Nested(USER_FIELDS, allow_null = True)
    }
    
    TOKEN_ARGS = {
        'token_only': Arg(required = False, default = True, use = boolean())
    }

    # GET a new token from a valid token
    @use_kwargs(TOKEN_ARGS, locations = ['query'])
    @marshal_with(AUTH_FIELDS)
    def get(self, token_only):
        print('token get(%s)' % token_only)
        token = g.user.generate_auth_token()
        return { 'token': token.decode('ascii'), 'renew_before': 550, 'user': None if token_only else g.user }
