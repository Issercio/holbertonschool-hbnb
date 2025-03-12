from flask import Flask
from flask_restx import Api
from app.extensions import db, bcrypt, jwt

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importation des modèles après l'initialisation des extensions
    from app.models import User, Place, Review, Amenity

    # Création des tables dans le contexte de l'application
    with app.app_context():
        db.create_all()

    api = Api(
        app, 
        version='1.0', 
        title='HBNB API', 
        description='HBNB Application API', 
        doc='/api/v1/'
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
