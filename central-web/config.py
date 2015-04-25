import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PORT = 8080
    HOST = '127.0.0.1'
    BOOTSTRAP_SERVE_LOCAL = True

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 't0p s3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class DemoConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEMO_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-demo.sqlite')

class TestingConfig(Config):
    SECRET_KEY = 'secret'
    HOST = '0.0.0.0'
    PORT = 80
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    HOST = '0.0.0.0'
    PORT = 80
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    BOOTSTRAP_SERVE_LOCAL = False

config = {
    'dev': DevelopmentConfig(),
    'test': TestingConfig(),
    'demo': DemoConfig(),
    'prod': ProductionConfig(),

    'default': DevelopmentConfig()
}

