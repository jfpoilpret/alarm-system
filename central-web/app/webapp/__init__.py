# encoding: utf-8

from flask import Blueprint

webapp = Blueprint('webapp', __name__)

from . import routes
