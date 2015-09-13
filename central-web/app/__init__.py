import os
from flask import Flask, redirect, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

monitoring_manager = None

def root():
    return redirect(url_for('monitor.signin'))

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

    from .monitor import monitor as monitor_blueprint
    app.register_blueprint(monitor_blueprint, url_prefix='/monitor')

    from .configure import configure as configure_blueprint
    app.register_blueprint(configure_blueprint, url_prefix='/configure')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .api_v1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix = '/api/1.0')

    from .webapp import webapp as webapp_blueprint
    app.register_blueprint(webapp_blueprint, url_prefix = '/webapp')    
    
    # Register the main route (redirect to login)
    app.add_url_rule('/', view_func = root)
    
    return app

