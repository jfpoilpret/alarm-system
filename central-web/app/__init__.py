import os
from flask import Flask, redirect, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.needs_refresh_message_category = 'info'

def after_request(response):
    # Store the current called URL for later use as return URL on cancel button
    if request.method == 'GET':
        session['return_url'] = request.url
    return response

def root():
    return redirect(url_for('auth.login'))

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

    # Add hook to remind the latest route (or URL) called so that we cancel button can return to it
    app.after_request(after_request)
    
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .monitor import monitor as monitor_blueprint
    app.register_blueprint(monitor_blueprint, url_prefix='/monitor')

    from .configure import configure as configure_blueprint
    app.register_blueprint(configure_blueprint, url_prefix='/configure')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # Register the main route (redirect to login)
    app.add_url_rule('/', view_func = root)

    return app

