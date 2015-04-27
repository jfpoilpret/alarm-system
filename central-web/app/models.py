# encoding: utf-8

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm.collections import attribute_mapped_collection
from . import db, login_manager

# Domain Model (DB Mapping)
#===========================

# ACCOUNT
#--------
class Account(UserMixin, db.Model):
    ROLE_ADMINISTRATOR = 1
    ROLE_CONFIGURATOR = 2
    ROLE_ALARM_SETTER = 3
    ROLE_ALARM_VIEWER = 4
    
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128), nullable=False, unique=True, index=True)
#    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    role = db.Column(db.Integer, nullable=False, default=ROLE_ALARM_VIEWER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == Account.ROLE_ADMINISTRATOR
    
    def is_configurator(self):
        return self.role in [Account.ROLE_ADMINISTRATOR, Account.ROLE_CONFIGURATOR]
    
    def is_alarm_setter(self):
        return self.role in [Account.ROLE_ADMINISTRATOR, Account.ROLE_CONFIGURATOR, Account.ROLE_ALARM_SETTER]
    
    def __repr__(self):
        return 'Account(id = %d, username = %s, role = %d)' % (self.id, self.username, self.role)

# LoginManager hook to get Account object from userid
@login_manager.user_loader
def load_user(userid):
    return Account.query.get(int(userid))

# CONFIGURATION
#--------------
class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    current = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    lockcode = db.Column(db.String(6), nullable=False)
    #TODO ensure cascaded delete of devices
    devices = db.relationship('Device', collection_class = attribute_mapped_collection('device_id'), lazy='select')
    #TODO other configuration (eg map picture...)

# DEVICE
#-------
class Device(db.Model):
    KIND_KEYPAD = 1
    KIND_MOTION = 2
    KIND_CAMERA = 3
    
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True, index=True)
    kind = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.Integer, nullable=False)
    voltage_threshold = db.Column(db.Float, nullable=True)
    config_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))
    #TODO other attributes (eg (x,y) location on map)

# ALERT
#------
class Alert(db.Model):
    LEVEL_INFO = 1
    LEVEL_WARNING = 2
    LEVEL_ALARM = 3
    
    __tablename__ = 'alert'
    id = db.Column(db.Integer, primary_key=True)
    config_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))
    
    when = db.Column(db.DateTime, nullable=False, index=True)
    level = db.Column(db.Integer, nullable=False, index=True)
    #TODO Define alert types somewhere
    alert_type = db.Column(db.Integer, nullable=False, index=True)
    message = db.Column(db.String(500))
    # TODO need true device reference
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    # TODO blob for pickled information?
