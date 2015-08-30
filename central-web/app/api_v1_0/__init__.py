from flask import Blueprint, request, g
from flask_restful import abort, Api
from webargs.flaskparser import parser

# Create blueprint for Web Services
api = Blueprint('api', __name__)

restApi = Api(api)

#TODO ensure authentication (with token)

# Register error handler for webargs
@parser.error_handler
def handle_webargs_error(err):
    # TODO currently only one error is thrown at first mistake (webargs issue)
    code = getattr(err, 'status_code', 400)
    msg = getattr(err, 'message', 'Invalid Request')
    name = getattr(err, 'arg_name', None)
    if name:
        abort(code, message = {name: msg})
    else:
        abort(code, message = msg)

# Register all REST resources
from .resources import UserResource, UsersResource
restApi.add_resource(UsersResource, '/users', endpoint = 'users')
restApi.add_resource(UserResource, '/users/<int:id>', endpoint = 'user')

from .resources import ConfigurationResource, ConfigurationsResource
restApi.add_resource(ConfigurationsResource, '/configurations', endpoint = 'configurations')
restApi.add_resource(ConfigurationResource, '/configurations/<int:id>', endpoint = 'configuration')

from .resources import ConfigurationMapResource
restApi.add_resource(ConfigurationMapResource, '/configurations/<int:id>/map', endpoint = 'map')

from .resources import CurrentConfigurationResource
restApi.add_resource(CurrentConfigurationResource, '/configurations/current', endpoint = 'current')

from .resources import DeviceResource, DevicesResource
restApi.add_resource(DevicesResource, '/configurations/<int:id>/devices', endpoint = 'devices')
restApi.add_resource(DeviceResource, '/devices/<int:id>', endpoint = 'device')

from .resources import NoPingAlertThresholdsResource
restApi.add_resource(NoPingAlertThresholdsResource, 
    '/configurations/<int:id>/alert-thresholds/no-ping', endpoint = 'no-ping')

from .resources import VoltageAlertThresholdsResource
restApi.add_resource(VoltageAlertThresholdsResource, 
    '/configurations/<int:id>/alert-thresholds/voltage', endpoint = 'voltage')

#TODO register missing REST resources for monitoring
