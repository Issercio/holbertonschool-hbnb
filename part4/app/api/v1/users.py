from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from werkzeug.exceptions import BadRequest
from app.models.user import User as UserModel
from app.extensions import db

api = Namespace('users', description='User operations')

# Modèle pour la création ou la mise à jour d'un utilisateur
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user, max 50 characters',
        min_length=1,
        max_length=50,
        example='John'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user, max 50 characters',
        min_length=1,
        max_length=50,
        example='Doe'
    ),
    'email': fields.String(
        required=True,
        description='Email of the user',
        example='john.doe@example.com'
    ),
    'password': fields.String(
        required=True,
        description='Password of the user',
        example='securepassword123'
    ),
    'is_admin': fields.Boolean(
        required=False,
        description='Admin status of the user',
        default=False
    )
})

# Modèle pour la réponse utilisateur
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User unique identifier'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Timestamp of user creation'),
    'updated_at': fields.DateTime(description='Timestamp of last update')
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.doc('list_users', security='Bearer')
    @api.marshal_with(api.model('UserListResponse', {
        'items': fields.List(fields.Nested(user_response_model)),
        'total': fields.Integer,
        'page': fields.Integer,
        'per_page': fields.Integer
    }))
    @api.param('page', 'Page number', type=int, default=1)
    @api.param('per_page', 'Items per page', type=int, default=10)
    def get(self):
        """List all users (Admin only)"""
        current_user_claims = get_jwt()
        
        # Vérification des privilèges administrateur
        if not current_user_claims.get('is_admin', False):
            api.abort(403, "Admin privileges required")
        
        # Pagination des utilisateurs
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        users, total = facade.get_users(page=page, per_page=per_page)
        
        # Convertir chaque utilisateur en dictionnaire si nécessaire
        user_dicts = [user.to_dict() if isinstance(user, UserModel) else user for user in users]
        
        return {
            'items': user_dicts,
            'total': total,
            'page': page,
            'per_page': per_page
        }

    @jwt_required()
    @api.doc('create_user', security='Bearer')
    @api.expect(user_model)
    @api.response(201, 'User created successfully', user_response_model)
    @api.response(400, 'Validation Error')
    @api.response(403, 'Admin privileges required')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Create a new user (Admin only)"""
        current_user_claims = get_jwt()
        
        # Vérification des privilèges administrateur
        if not current_user_claims.get('is_admin', False):
            api.abort(403, "Admin privileges required")
        
        try:
            # Valider les données avant la création
            data = api.payload
            
            # Vérifier si l'email est unique
            existing_user = db.session.query(UserModel).filter_by(email=data['email']).first()
            if existing_user:
                return {"message": "email already used"}, 400
            
            new_user = facade.create_user(data)
            
            if new_user is None or not new_user.id:
                return {"message": "Failed to create user"}, 500
            
            return new_user.to_dict(), 201
        
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            return {"message": f"An unexpected error occurred: {str(e)}"}, 500

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @jwt_required()
    @api.doc('get_user', security='Bearer')
    @api.marshal_with(user_response_model, mask=False)
    def get(self, user_id):
        """Get a user by ID."""
        
        # Récupération des revendications du token JWT
        current_user_claims = get_jwt()
        
        # Vérification des permissions : admin ou propriétaire du compte
        if not current_user_claims.get('is_admin', False) and user_id != get_jwt_identity():
            api.abort(403, "Unauthorized action")
        
        # Récupération de l'utilisateur
        user = facade.get_user(user_id)
        
        if not user:
            api.abort(404, f"User {user_id} not found")
        
        return user.to_dict()

    @jwt_required()
    @api.doc('update_user', security='Bearer')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, mask=False)
    @api.response(400, 'Validation Error')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Update a user (Admin or Owner)."""
        
        # Récupération des revendications du token JWT
        current_user_claims = get_jwt()
        
        # Vérification des permissions : admin ou propriétaire du compte
        if not current_user_claims.get('is_admin', False) and user_id != get_jwt_identity():
            api.abort(403, "Unauthorized action")
        
        try:
            # Admin peut tout modifier; propriétaire ne peut pas modifier certains champs sensibles
            if current_user_claims.get('is_admin', False):
                update_data = api.payload
            else:
                allowed_fields = ['first_name', 'last_name', 'password']
                update_data = {k: v for k, v in api.payload.items() if k in allowed_fields}
            
            if not update_data:
                api.abort(400, "No valid fields to update")
            
            updated_user = facade.update_user(user_id, update_data)
            
            if not updated_user:
                api.abort(404, f"User {user_id} not found")
            
            return updated_user.to_dict()
        
        except ValueError as e:
            api.abort(400, str(e))
