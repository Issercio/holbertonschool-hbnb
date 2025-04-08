import os
from datetime import timedelta

class Config:
    """Base configuration class.
    
    Contains default configuration settings for the application.
    All other configuration classes inherit from this class.
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')  # Clé secrète par défaut
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Désactive le suivi des modifications SQLAlchemy (meilleures performances)
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)  # Utilise SECRET_KEY si JWT_SECRET_KEY n'est pas défini
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Durée de vie des tokens d'accès (1 heure)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Durée de vie des tokens de rafraîchissement (30 jours)
    JWT_TOKEN_LOCATION = ['headers']  # Utilisation des headers pour transmettre les tokens
    JWT_COOKIE_CSRF_PROTECT = False  # Désactiver la protection CSRF pour simplifier les tests

class DevelopmentConfig(Config):
    """Development configuration settings.
    
    Used for local development with debugging enabled.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///development.db')  # Base de données SQLite par défaut

class TestingConfig(Config):
    """Testing configuration settings.
    
    Used for running tests with testing mode enabled.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///testing.db')  # Base de données SQLite pour tests
    
    # Shorter token expiration for testing
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)  # Tokens expirent après 15 minutes
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)  # Tokens de rafraîchissement expirent après 1 heure

class ProductionConfig(Config):
    """Production configuration settings.
    
    Used for deployment in production environment.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///production.db')  # Base de données SQLite par défaut en production
    
    # Use a separate secret key for JWT in production
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # Clé secrète pour les tokens JWT en production

def validate_config(app):
    """Validate critical configuration settings."""
    if not app.config['JWT_SECRET_KEY']:
        raise ValueError("JWT_SECRET_KEY is not set in the environment variables.")
    
    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("SQLALCHEMY_DATABASE_URI is not set in the environment variables.")
