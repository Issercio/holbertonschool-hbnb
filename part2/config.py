import os

class Config:
    """Base configuration class.
    
    Contains default configuration settings for the application.
    All other configuration classes inherit from this class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hbnb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration settings.
    
    Used for local development with debugging enabled.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'

class TestingConfig(Config):
    """Testing configuration settings.
    
    Used for running tests with testing mode enabled.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_test.db'

class ProductionConfig(Config):
    """Production configuration settings.
    
    Used for deployment in production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hbnb_prod.db'

