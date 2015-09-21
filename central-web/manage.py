#!/usr/bin/env python
# encoding: utf-8

from app import create_app
from flask_script import Manager, Server
from app import db
from app.models import Account
from config import config

manager = Manager(create_app)

# Available commands in command-line
@manager.command
def adduser(username, fullname = None, role = Account.ROLE_ALARM_VIEWER):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    if not fullname:
        fullname = username
    db.create_all()
    user = Account(
        username=username, 
        fullname=fullname, 
        password=password,
        role=role)
    db.session.add(user)
    db.session.commit()
    print('Account {0} was registered successfully.'.format(username))

@manager.command
def resetdb():
    """Reset current Database and prepare for training (i.e. just one admin user 'admin' (pw. admin))"""
    db.drop_all()
    db.create_all()
    db.session.add(
        Account(
            username='admin', 
            fullname = u'Administrator', 
            password='admin', 
            role=Account.ROLE_ADMINISTRATOR))
    db.session.commit()
    print('User `admin` was registered successfully.')

# Wrapper to flask-script Server so that port can be read from app.config by default (after manager.run() is called)
def replace_port_option(o):
    if o.kwargs['dest'] == 'port':
        o.kwargs['default'] = -1
    elif o.kwargs['dest'] == 'host':
        o.kwargs['default'] = '999.999.999.999'
    return o

class ConfigServer(Server):
    def get_options(self):
        options = super(ConfigServer, self).get_options()
        return map(replace_port_option, options)
  
    def __call__(self, app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors):
        if port == -1:
            port = app.config['PORT']
        if host == '999.999.999.999':
            host = app.config['HOST']
        # Initialize MonitoringManager and activate it if needed
        from app.monitor.monitoring import MonitoringManager
        from app.models import Configuration
        Account.init(app)
        monitoring_manager = MonitoringManager.create(app)
        with app.app_context():
            active = Configuration.query.filter_by(active = True).first()
            if active:
                monitoring_manager.activate(active)
            
        super(ConfigServer, self).__call__(app, host, port, use_debugger, use_reloader, threaded, processes, passthrough_errors)

# MAIN START
if __name__ == '__main__':
    manager.add_option('-c', '--config', metavar = 'CONFIG', dest = 'config_name', required = False, choices = config.keys())
    manager.add_command('runserver', ConfigServer())
    manager.run()
