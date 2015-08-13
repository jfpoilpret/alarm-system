from flask import Blueprint, request, g
from flask_restful import Api

# Create blueprint for Web Services
api = Blueprint('api', __name__)

restApi = Api(api)

#TODO ensure authentication (with token)

#TODO register all REST resources
from .resources import User, Users

restApi.add_resource(Users, '/users', endpoint = 'users')
restApi.add_resource(User, '/users/<int:id>', endpoint = 'user')
