from flask import Flask, jsonify
from flask_restx import Api
from app.extensions import db, bcrypt, jwt
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

def create_app(config_class="config.DevelopmentConfig"):
    """
    Crée et configure l'application Flask.
    
    Args:
        config_class (str): Chemin vers la classe de configuration à utiliser.
            Par défaut, "config.DevelopmentConfig".
    
    Returns:
        Flask: L'application Flask configurée.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configuration spécifique JWT
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'fallback-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    # Initialisation des extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    # Configuration du gestionnaire JWT
    jwt_manager = JWTManager(app)

    @jwt_manager.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "Token has expired"}), 401

    @jwt_manager.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Invalid token"}), 401

    # Importation des modèles après l'initialisation des extensions
    from app.models import User, Place, Review, Amenity

    api = Api(
        app, 
        version='1.0', 
        title='HBNB API', 
        description='HBNB Application API', 
        doc='/api/v1/',
        authorizations={
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
            }
        },
        security='Bearer'
    )

    # Import des namespaces
    from .api.v1.users import api as users_ns
    from .api.v1.auth import api as auth_ns
    from .api.v1.amenities import api as amenities_ns
    from .api.v1.places import api as places_ns
    from .api.v1.reviews import api as reviews_ns

    # Register namespaces
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(amenities_ns)
    api.add_namespace(places_ns)
    api.add_namespace(reviews_ns)

    return app
