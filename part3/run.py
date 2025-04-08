import os
import logging
from app import create_app
from config import validate_config

"""Entry point for running the Flask application.

This module creates and configures the Flask application instance using
the create_app factory function. When run directly, it starts the 
development server on localhost port 5000 with debug mode enabled.
"""

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application Flask
app = create_app()

# Validation des configurations critiques
validate_config(app)

if __name__ == '__main__':
    # Gestion des environnements
    environment = os.environ.get('FLASK_ENV', 'development')
    debug = environment == 'development'

    logger.info(f"Starting Flask application in {environment} mode...")
    app.run(host='127.0.0.1', port=5000, debug=debug)
