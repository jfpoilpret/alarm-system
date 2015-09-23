# encoding: utf-8

from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import deferred
from sqlalchemy.orm.collections import attribute_mapped_collection
from . import db
from sqlalchemy.sql.schema import UniqueConstraint

# Domain Model (DB Mapping)
#===========================

# ACCOUNT
#--------
class Account(db.Model):
    secret = None
    revoked_tokens = []
    
    ROLE_ADMINISTRATOR = 1
    ROLE_CONFIGURATOR = 2
    ROLE_ALARM_SETTER = 3
    ROLE_ALARM_VIEWER = 4
    
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), nullable = False, unique = True, index = True)
    password_hash = db.Column(db.String(128))
    fullname = db.Column(db.String(128), nullable = False, unique = True, index = True)
#    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    role = db.Column(db.Integer, nullable = False, default = ROLE_ALARM_VIEWER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def init(app):
        Account.secret = app.config['SECRET_KEY']
    
    def generate_auth_token(self, expiration = 600):
        s = Serializer(Account.secret, expires_in = expiration)
        return s.dumps({ 'id': self.id })
    
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Account.secret)
        try:
            data = s.loads(token)
        except SignatureExpired:
            if token in Account.revoked_tokens:
                Account.revoked_tokens.remove(token)
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        # Extra check that token is not currently revoked
        if token in Account.revoked_tokens:
            return None
        user = Account.query.get(data['id'])
        return user
    
    @staticmethod
    def revoke_token(token):
        Account.revoked_tokens.append(token)
    
    #TODO need to ensure this method is called often enough, to remove expired tokens from list
    @staticmethod
    def clear_expired_revoked_tokens():
        s = Serializer(Account.secret)
        for token in Account.revoked_tokens:
            try:
                s.loads(token)
            except SignatureExpired:
                Account.revoked_tokens.remove(token)
    
    def is_admin(self):
        return self.role == Account.ROLE_ADMINISTRATOR
    
    def is_configurator(self):
        return self.role in [Account.ROLE_ADMINISTRATOR, Account.ROLE_CONFIGURATOR]
    
    def is_alarm_setter(self):
        return self.role in [Account.ROLE_ADMINISTRATOR, Account.ROLE_CONFIGURATOR, Account.ROLE_ALARM_SETTER]
    
    def __repr__(self):
        return 'Account(id = %d, username = %s, role = %d)' % (self.id, self.username, self.role)

# CONFIGURATION
#--------------
class Configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, unique = True, index = True)
    current = db.Column(db.Boolean, nullable = False, default = False)
    active = db.Column(db.Boolean, nullable = False, default = False)
    lockcode = db.Column(db.String(6), nullable = False)
    devices = db.relationship('Device', 
        collection_class = attribute_mapped_collection('device_id'), 
        cascade = 'all, delete-orphan', lazy = 'select')
    map_area = deferred(db.Column(db.Text, nullable = True))
    map_area_filename = db.Column(db.String(256), nullable = True)
    no_ping_time_alert_thresholds = db.relationship('NoPingTimeAlertThreshold', 
        cascade = 'all, delete-orphan', lazy = 'select')
    voltage_rate_alert_thresholds = db.relationship('VoltageRateAlertThreshold', 
        cascade = 'all, delete-orphan', lazy = 'select')

    def __repr__(self):
        return 'Configuration(id = %s, name = %s, current = %s, active = %s, file = %s)' % (
            str(self.id), self.name, self.current, self.active, self.map_area_filename)

# DEVICE
#-------
class Device(db.Model):
    KIND_KEYPAD = 1
    KIND_MOTION = 2
    KIND_CAMERA = 3
    
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, index = True)
    kind = db.Column(db.Integer, nullable = False)
    device_id = db.Column(db.Integer, nullable = False, index = True)
    voltage_threshold = db.Column(db.Float, nullable = True)
    config_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))
    location_x = db.Column(db.Float, nullable = True)
    location_y = db.Column(db.Float, nullable = True)
    # Additional constraints
    index1 = UniqueConstraint(config_id, device_id)
    index2 = UniqueConstraint(config_id, name)
    
    def detached(self):
        class Copy(object):
            pass
        copy = Copy()
        copy.id = self.id
        copy.name = self.name
        copy.kind = self.kind
        copy.device_id = self.device_id
        copy.voltage_threshold = self.voltage_threshold
        copy.config_id = self.config_id
        copy.location_x = self.location_x
        copy.location_y = self.location_y
        return copy

class NoPingTimeAlertThreshold(db.Model):
    __tablename__ = 'no_ping_time_threshold'
    id = db.Column(db.Integer, primary_key = True)
    config_id = db.Column(db.Integer, db.ForeignKey('configuration.id'), nullable = False)
    alert_level = db.Column(db.Integer, nullable = False)
    alert_time = db.Column(db.Integer, nullable = False)

class VoltageRateAlertThreshold(db.Model):
    __tablename__ = 'voltage_rate_threshold'
    id = db.Column(db.Integer, primary_key = True)
    config_id = db.Column(db.Integer, db.ForeignKey('configuration.id'), nullable = False)
    alert_level = db.Column(db.Integer, nullable = False)
    alert_time = db.Column(db.Integer, nullable = False)
    voltage_rate = db.Column(db.Integer, nullable = False)

#TODO Define alert types somewhere
#TODO Improve to include LEVEL with each KIND
class AlertType(object):
    DEVICE_VOLTAGE_UNDER_THRESHOLD = 1
    DEVICE_NO_PING_FOR_TOO_LONG = 2
    LOCK = 3
    UNLOCK = 4
    WRONG_LOCK_CODE = 5
    SYSTEM_ACTIVATION = 6
    SYSTEM_DEACTIVATION = 7

# ALERT
#------
class Alert(db.Model):
    LEVEL_INFO = 1
    LEVEL_WARNING = 2
    LEVEL_ALARM = 3
    
    __tablename__ = 'alert'
    id = db.Column(db.Integer, primary_key = True)
    config_id = db.Column(db.Integer, db.ForeignKey('configuration.id'))
    
    when = db.Column(db.DateTime, nullable = False, index = True)
    level = db.Column(db.Integer, nullable = False, index = True)
    alert_type = db.Column(db.Integer, nullable = False, index = True)
    message = db.Column(db.String(500))
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))
    device = db.relationship(Device, cascade = 'delete', lazy = 'select')
    # TODO blob for pickled information?
