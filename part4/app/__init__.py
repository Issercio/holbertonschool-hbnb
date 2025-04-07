from flask import Flask, render_template, jsonify
from flask_restx import Api
from app.extensions import db, bcrypt, jwt
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from app.models.user import User

def create_app(config_class="config.DevelopmentConfig"):
    """
    Crée et configure l'application Flask.
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

    # API REST avec flask-restx
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
                'description': "Type in the *'Value'* input box below: **'Bearer <JWT>'**, where JWT is the token"
            }
        },
        security='Bearer'
    )

    # Import des namespaces pour l'API REST
    from .api.v1.users import api as users_ns
    from .api.v1.auth import api as auth_ns
    from .api.v1.amenities import api as amenities_ns
    from .api.v1.places import api as places_ns
    from .api.v1.reviews import api as reviews_ns

    # Enregistrement des namespaces dans l'API REST
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(amenities_ns)
    api.add_namespace(places_ns)
    api.add_namespace(reviews_ns)

    # Routes HTML pour les pages web
    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/place')
    def place():
        return render_template('place.html')

    @app.route('/add_review')
    def add_review():
        return render_template('add_review.html')

    # Gestion des erreurs 404 (page non trouvée)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Initialisation de la base de données et création de l'utilisateur admin
    with app.app_context():
        db.create_all()
        
        # Création de l'utilisateur admin si nécessaire
        admin_email = "admin@hbnb.io"
        admin_password = "admin1234"
        if not User.query.filter_by(email=admin_email).first():
            hashed_password = generate_password_hash(admin_password)  # Hash du mot de passe
            admin_user = User(
                first_name="Admin",
                last_name="User",
                email=admin_email,
                password=hashed_password,
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()

    return app
