from flask import Blueprint

configure = Blueprint('configure', __name__)

from . import routes
