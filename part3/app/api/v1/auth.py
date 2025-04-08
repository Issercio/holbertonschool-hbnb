from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity
)
from app.services import facade
from functools import wraps
from app.models.user import User
from flask import jsonify, request
from app.extensions import db

api = Namespace('auth', description='Authentication operations')

# Modèle pour valider les données d'entrée de connexion
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='Access token'),
    'refresh_token': fields.String(description='Refresh token')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_model)
    @api.response(200, 'Success')
    @api.response(400, 'Missing email or password')
    @api.response(401, 'Invalid credentials')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Authentifier l'utilisateur et retourner un token JWT"""
        credentials = api.payload or {}
        
        # Vérification des champs requis
        if 'email' not in credentials or 'password' not in credentials:
            return {"message": "Missing email or password"}, 400
        
        try:
            user = facade.get_user_by_email(credentials['email'])
            
            # Vérification explicite que l'objet retourné est bien une instance de User
            if not user or not isinstance(user, User):
                return {"message": "Invalid credentials"}, 401
            
            if not user.verify_password(credentials['password']):
                return {"message": "Invalid credentials"}, 401

            # Création des tokens (access et refresh)
            access_token = create_access_token(identity=user.id, additional_claims={'is_admin': user.is_admin})
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        
        except Exception as e:
            return {"message": f"An internal error occurred: {str(e)}"}, 500


@api.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Rafraîchir le token d'accès"""
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return {"access_token": access_token}, 200


@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """Déconnecter l'utilisateur (placeholder)"""
        # Implémentation future : Ajouter le token à une liste de révocation.
        return {"message": "Logout successful"}, 200


def token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"msg": "Missing or invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


def init_admin_user():
    """Initialize admin user if not exists"""
    admin_email = "admin@hbnb.io"
    admin_password = "admin1234"
    
    try:
        admin_user = facade.get_user_by_email(admin_email)
        if not admin_user:
            admin_user = User(
                first_name="Admin",
                last_name="User",
                email=admin_email,
                is_admin=True
            )
            # Hachage du mot de passe avant de le sauvegarder
            admin_user.set_password(admin_password)
            
            db.session.add(admin_user)
            db.session.commit()
        else:
            pass  # Admin user already exists; no action needed.
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error initializing admin user: {str(e)}")
