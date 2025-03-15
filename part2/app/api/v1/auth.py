from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from functools import wraps
from flask import jsonify, current_app

api = Namespace('auth', description='Authentication operations')

# Modèle pour valider les données d'entrée de connexion
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

token_model = api.model('Token', {
    'access_token': fields.String(description='Access token')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.marshal_with(token_model)
    @api.response(200, 'Success')
    @api.response(401, 'Invalid credentials')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Authentifier l'utilisateur et retourner un token JWT"""
        credentials = api.payload
        
        try:
            current_app.logger.info(f"Login attempt for email: {credentials['email']}")
            user = facade.get_user_by_email(credentials['email'])
            
            if not user:
                current_app.logger.warning(f"No user found for email: {credentials['email']}")
                return {"message": "Invalid credentials"}, 401
            
            if not user.verify_password(credentials['password']):
                current_app.logger.warning(f"Invalid password for user: {credentials['email']}")
                return {"message": "Invalid credentials"}, 401

            access_token = create_access_token(identity=user.id, additional_claims={'is_admin': user.is_admin})
            current_app.logger.info(f"Successful login for user: {credentials['email']}")
            return {'access_token': access_token}, 200
        
        except Exception as e:
            current_app.logger.error(f"An error occurred during login: {str(e)}")
            return {"message": "An internal error occurred"}, 500

@api.route('/logout')
class Logout(Resource):
    @jwt_required()
    @api.response(200, 'Successfully logged out')
    @api.response(401, 'Unauthorized')
    def post(self):
        """Déconnecter l'utilisateur (invalider le token)"""
        jti = get_jwt()["jti"]
        # Ici, vous devriez ajouter le JTI à une liste noire
        # Cette implémentation dépend de votre stratégie de stockage (Redis, base de données, etc.)
        # Pour l'exemple, nous allons simplement retourner un message de succès
        current_app.logger.info(f"User logged out: {get_jwt_identity()}")
        return {"message": "Successfully logged out"}, 200

@api.route('/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @api.response(200, 'Token refreshed successfully')
    @api.response(401, 'Unauthorized')
    def post(self):
        """Rafraîchir le token d'accès"""
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        current_app.logger.info(f"Token refreshed for user: {current_user}")
        return {"access_token": new_token}, 200

def token_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user = get_jwt_identity()
        if not current_user:
            current_app.logger.warning("Missing or invalid token")
            return jsonify({"msg": "Missing or invalid token"}), 401
        return f(*args, **kwargs)
    return decorated
