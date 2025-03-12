from flask_restx import Namespace, Resource, fields
from app.services import facade
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import IntegrityError
import uuid

api = Namespace('users', description='User operations')

class UUIDField(fields.String):
    def format(self, value):
        try:
            uuid.UUID(str(value))
            return str(value)
        except ValueError:
            raise ValueError('Invalid UUID')

# Modèle mis à jour avec validation étendue
user_model = api.model('User', {
    'first_name': fields.String(required=True, max_length=50, example='John'),
    'last_name': fields.String(required=True, max_length=50, example='Doe'),
    'email': fields.String(required=True, pattern=r'^\S+@\S+\.\S+$', example='john.doe@example.com'),
    'is_admin': fields.Boolean(default=False)
})

user_response_model = api.model('UserResponse', {
    'id': UUIDField(required=True, description='ID unique'),
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'is_admin': fields.Boolean,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
})

@api.route('/')
class UserList(Resource):
    @api.marshal_list_with(user_response_model)
    def get(self):
        """List all users with pagination"""
        try:
            return facade.get_users()
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(user_model)
    @api.marshal_with(user_response_model, code=201)
    @api.response(400, 'Invalid input')
    @api.response(409, 'Duplicate email')
    def post(self):
        """Create user with data validation"""
        try:
            data = api.payload
            if not all(key in data for key in ['first_name', 'last_name', 'email']):
                raise BadRequest('Missing required fields')
                
            return facade.create_user(data), 201
            
        except IntegrityError as e:
            api.abort(409, 'Email already exists')
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, 'Server error: ' + str(e))

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier (UUID)')
class UserResource(Resource):
    @api.marshal_with(user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID with proper type checking"""
        try:
            user = facade.get_user(user_id)
            if not user:
                api.abort(404, f'User {user_id} not found')
            return user
        except Exception as e:
            api.abort(500, str(e))

    @api.expect(user_model)
    @api.marshal_with(user_response_model)
    @api.response(400, 'Invalid input')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user with full validation"""
        try:
            data = api.payload
            if 'email' in data:
                existing = facade.get_user_by_email(data['email'])
                if existing and str(existing['id']) != user_id:
                    api.abort(409, 'Email already in use')
                    
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                api.abort(404, f'User {user_id} not found')
                
            return updated_user
            
        except IntegrityError as e:
            api.abort(409, 'Database constraint error')
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, 'Server error: ' + str(e))
