import os

class Config:
    """Base configuration class.
    
    Contains default configuration settings for the application.
    All other configuration classes inherit from this class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive le suivi des modifications SQLAlchemy (meilleures performances)

class DevelopmentConfig(Config):
    """Development configuration settings.
    
    Used for local development with debugging enabled.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///development.db')

class TestingConfig(Config):
    """Testing configuration settings.
    
    Used for running tests with testing mode enabled.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///testing.db')

class ProductionConfig(Config):
    """Production configuration settings.
    
    Used for deployment in production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///production.db')
