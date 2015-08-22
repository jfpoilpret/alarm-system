from flask import Blueprint, request, g
from flask_restful import Api

# Create blueprint for Web Services
api = Blueprint('api', __name__)

restApi = Api(api)

#TODO ensure authentication (with token)

#TODO register all REST resources
from .resources import UserResource, UsersResource
restApi.add_resource(UsersResource, '/users', endpoint = 'users')
restApi.add_resource(UserResource, '/users/<int:id>', endpoint = 'user')

from .resources import ConfigurationResource, ConfigurationsResource
restApi.add_resource(ConfigurationsResource, '/configurations', endpoint = 'configurations')
restApi.add_resource(ConfigurationResource, '/configurations/<int:id>', endpoint = 'configuration')

from .resources import ConfigurationMapResource
restApi.add_resource(ConfigurationMapResource, '/configurations/<int:id>/map', endpoint = 'map')

#TODO allow get/set current
from .resources import CurrentConfigurationResource
restApi.add_resource(CurrentConfigurationResource, '/configurations/current', endpoint = 'current')

from .resources import DeviceResource, DevicesResource
restApi.add_resource(DevicesResource, '/configurations/<int:id>/devices', endpoint = 'devices')
restApi.add_resource(DeviceResource, '/devices/<int:id>', endpoint = 'device')

