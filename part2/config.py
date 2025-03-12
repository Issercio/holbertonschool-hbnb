import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 280,
        'pool_timeout': 20,
        'pool_size': 10,
        'max_overflow': 5,
    }
    PROPAGATE_EXCEPTIONS = True
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    """Development configuration settings."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Testing configuration settings."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"

class ProductionConfig(Config):
    """Production configuration settings."""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///production.db")
    SQLALCHEMY_ECHO = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
