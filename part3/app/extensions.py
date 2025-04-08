from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Extensions Flask
db = SQLAlchemy()  # Gestion des bases de données avec SQLAlchemy
bcrypt = Bcrypt()  # Gestion des mots de passe (hashing et vérification)
jwt = JWTManager()  # Gestion des tokens JWT

def init_app(app):
    """
    Initialise toutes les extensions avec l'application Flask.
    
    Args:
        app (Flask): Instance de l'application Flask.
    
    Raises:
        ValueError: Si l'application Flask n'est pas correctement configurée.
    """
    if not app:
        raise ValueError("L'application Flask n'est pas définie.")
    
    # Initialisation des extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
