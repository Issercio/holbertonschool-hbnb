from flask import Flask
from flask_restx import Api
from .api.v1.users import api as users_ns
from .api.v1.amenities import api as amenities_ns
from .api.v1.places import api as places_ns
from .api.v1.reviews import api as reviews_ns
from app.models import db  # Assurez-vous que cette importation est correcte

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # Charger la configuration depuis l'objet spécifié
    app.config.from_object(config_class)
    
    # Initialiser SQLAlchemy avec l'application
    db.init_app(app)
    
    api = Api(
        app, 
        version='1.0', 
        title='HBNB API', 
        description='HBNB Application API', 
        doc='/api/v1/'
    )

    # Register namespaces
    api.add_namespace(users_ns)
    api.add_namespace(amenities_ns)
    api.add_namespace(places_ns)
    api.add_namespace(reviews_ns)

    # Création des tables (uniquement en développement)
    with app.app_context():
        db.create_all()

    return app
