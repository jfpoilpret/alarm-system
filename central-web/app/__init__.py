# encoding: utf-8

import os
from flask import Flask, g, jsonify, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

# Authentication Management
# Note: we use a "Dummy" scheme to avoid browser popping up its own dialog when receiving 401
auth = HTTPBasicAuth(scheme = 'Dummy', realm = 'None')

@auth.error_handler
def auth_error_handler():
    res = jsonify(message = 'Invalid credentials')
    res.status_code = 401
    return res

from .models import Account

@auth.verify_password
def verify_token(user_or_token, password):
    user = Account.verify_auth_token(user_or_token)
    if not user:
        g.token = None
        user = Account.query.filter_by(username = user_or_token).first()
        if user and not user.verify_password(password):
            user = None
    else:
        g.token = user_or_token
    g.user = user
    return (user is not None)

monitoring_manager = None

def root():
    return redirect(url_for('webapp.signin'))

def create_app(config_name = None):
    app = Flask(__name__)
    if not config_name:
        config_name = os.getenv('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production
        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    bootstrap.init_app(app)
    db.init_app(app)

    from .api_v1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix = '/api/1.0')

    from .webapp import webapp as webapp_blueprint
    app.register_blueprint(webapp_blueprint, url_prefix = '/webapp')    
    
    # Register the main route (redirect to login)
    app.add_url_rule('/', view_func = root)
    
    return app
