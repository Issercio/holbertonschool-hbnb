from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from functools import wraps
from app.models.user import User
from flask import jsonify, current_app
from app.extensions import db

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
            current_app.logger.info(f"Login attempt for email: {credentials['email']}")
            user = facade.get_user_by_email(credentials['email'])
            
            # Vérification explicite que l'objet retourné est bien une instance de User
            if not user or not isinstance(user, User):
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
                password=admin_password,
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
            current_app.logger.info(f"Admin user created: {admin_email}")
        else:
            current_app.logger.info(f"Admin user already exists: {admin_email}")
    except Exception as e:
        current_app.logger.error(f"Error creating admin user: {str(e)}")
        db.session.rollback()
