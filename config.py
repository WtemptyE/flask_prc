import os

class Configuration(object):
    DEBUG = True
    APPLICATION_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(APPLICATION_DIR, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'flask blog'
    STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')
    IMAGES_DIR = os.path.join(STATIC_DIR, 'images')