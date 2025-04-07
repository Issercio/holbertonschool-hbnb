from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

api = Namespace('auth', description='Authentication operations')

# Modèle pour valider les données d'entrée de connexion
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Modèle pour la réponse contenant le token
token_model = api.model('Token', {
    'access_token': fields.String(description='Access token')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_model)
    @api.response(200, 'Success')
    @api.response(400, 'Missing email or password')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authentifier l'utilisateur et retourner un token JWT"""
        credentials = api.payload or {}

        # Vérification des champs requis
        if 'email' not in credentials or 'password' not in credentials:
            return {"message": "Missing email or password"}, 400

        # Récupérer l'utilisateur par email
        user = User.query.filter_by(email=credentials['email']).first()
        if not user or not user.verify_password(credentials['password']):
            return {"message": "Invalid credentials"}, 401

        # Générer un token JWT pour l'utilisateur
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

def init_admin_user():
    """Créer un utilisateur admin si nécessaire"""
    admin_email = "admin@hbnb.io"
    admin_password = "admin1234"

    # Vérifier si l'utilisateur admin existe déjà
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
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

# Appeler cette fonction dans ton fichier principal (run.py ou app/__init__.py)
