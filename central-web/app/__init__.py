import os
from flask import Flask, redirect, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from config import config
from flask.sessions import SessionInterface

bootstrap = Bootstrap()
db = SQLAlchemy()

monitoring_manager = None

# Special SessionManager to ensure no session is created (and no cookie)
#TODO check if this is really useful (maybe observed cookie was cached?)
class NoSessionManager(SessionInterface):
    def open_session(self, app, request):
        return None

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
    
    # Remove sessions
    Flask.session_interface = NoSessionManager()
    
    return app

