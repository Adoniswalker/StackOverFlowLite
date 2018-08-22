"""THis are the global configuration for application"""
import os


class BaseConfig(object):
    """This is a base class that contains configuration of all classes"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    DATABASE_URI = os.getenv("DATABASE_URL")
    DEBUG = True


class TestConfig(BaseConfig):
    """This is the testing environment"""
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(BaseConfig):
    """For development environment"""
    DEBUG = True


class ProductionConfig(BaseConfig):
    """For production enviroment"""
    DEBUG = True
