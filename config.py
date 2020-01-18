import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, .env))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-not-secret'

    DEBUG = os.environ.get('DEBUG') or FALSE

    #SQL Config
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = os.environ.get('SQLALCHEMY_POOL_RECYCLE') or 299

