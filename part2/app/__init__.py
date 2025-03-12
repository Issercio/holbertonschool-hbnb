from flask import Flask, jsonify
from flask_restx import Api
from .extensions import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialiser SQLAlchemy
    db.init_app(app)

    with app.app_context():
        # Importer les modèles ici pour éviter les importations circulaires
        from app.models.associations import place_amenity
        from app.models.user import User
        from app.models.place import Place
        from app.models.amenity import Amenity
        from app.models.review import Review
        
        # Crée les tables si elles n'existent pas encore
        db.create_all()

    # Configurer l'API RESTx
    api = Api(
        app,
        version='1.0',
        title='HBNB API',
        description='HBNB Application API',
        doc='/api/v1/'
    )

    # Importer et enregistrer les namespaces ici pour éviter les importations circulaires
    from .api.v1.users import api as users_ns
    from .api.v1.amenities import api as amenities_ns
    from .api.v1.places import api as places_ns
    from .api.v1.reviews import api as reviews_ns

    api.add_namespace(users_ns)
    api.add_namespace(amenities_ns)
    api.add_namespace(places_ns)
    api.add_namespace(reviews_ns)

    # Gestionnaire global pour IntegrityError
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        response = {
            "message": "Integrity constraint violated. Please check your data.",
            "details": str(error.orig)  # Inclure des détails sur l'erreur (facultatif)
        }
        return jsonify(response), 409

    # Gestionnaire global pour SQLAlchemyError (autres erreurs SQLAlchemy)
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        response = {
            "message": "A database error occurred.",
            "details": str(error)  # Inclure des détails sur l'erreur (facultatif)
        }
        return jsonify(response), 500

    return app
