from flask_restx import Namespace, Resource, fields
from app.services import facade
from werkzeug.exceptions import BadRequest
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('users', description='User operations')

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
    @api.doc('list_users')
    @api.marshal_list_with(user_response_model, mask=False)
    @api.param('page', 'Page number', type=int, default=1)
    @api.param('per_page', 'Items per page', type=int, default=10)
    def get(self):
        """List all users (Admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin', False):
            api.abort(403, "Admin privileges required")
        
        page = api.payload.get('page', 1)
        per_page = api.payload.get('per_page', 10)
        users, total = facade.get_users(page=page, per_page=per_page)
        return {
            'items': [user.to_dict() for user in users],
            'total': total,
            'page': page,
            'per_page': per_page
        }

    @jwt_required()
    @api.doc('create_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, code=201, mask=False)
    @api.response(400, 'Validation Error')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Create a new user (Admin only)"""
        current_user = get_jwt()
        if not current_user.get('is_admin', False):
            api.abort(403, "Admin privileges required")
        
        try:
            new_user = facade.create_user(api.payload)
            return new_user.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class User(Resource):
    @jwt_required()
    @api.doc('get_user')
    @api.marshal_with(user_response_model, mask=False)
    def get(self, user_id):
        """Get a user by ID."""
        current_user = get_jwt()
        if not current_user.get('is_admin', False) and user_id != get_jwt_identity():
            api.abort(403, "Unauthorized action")
        
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user.to_dict()

    @jwt_required()
    @api.doc('update_user')
    @api.expect(user_model)
    @api.marshal_with(user_response_model, mask=False)
    @api.response(400, 'Validation Error')
    @api.response(403, 'Unauthorized action')
    def put(self, user_id):
        """Update a user (Admin or Owner)."""
        current_user = get_jwt()
        if not current_user.get('is_admin', False) and user_id != get_jwt_identity():
            api.abort(403, "Unauthorized action")
        
        try:
            # Admin can update all fields, owner can't update email and is_admin
            if current_user.get('is_admin', False):
                update_data = api.payload
            else:
                update_data = {k: v for k, v in api.payload.items() if k not in ['email', 'is_admin']}
            
            if not update_data:
                api.abort(400, "No valid fields to update")
            
            updated_user = facade.update_user(user_id, update_data)
            if not updated_user:
                api.abort(404, f"User {user_id} not found")
            return updated_user.to_dict()
        except ValueError as e:
            api.abort(400, str(e))
