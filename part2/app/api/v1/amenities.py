from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Expanded amenity model for responses
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Unique identifier for the amenity'),
    'name': fields.String(description='Name of the amenity'),
    'created_at': fields.DateTime(description='Timestamp when the amenity was created'),
    'updated_at': fields.DateTime(description='Timestamp when the amenity was last updated'),
    'places': fields.List(fields.String(description='Place IDs with this amenity'))
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized')
    @api.marshal_with(amenity_response_model)
    def post(self):
        """Register a new amenity (Admin only)"""
        current_user = get_jwt_identity()
        user = facade.get_user(current_user)
        if not user.is_admin:
            return {'message': 'Admin privileges required'}, 403
        
        data = api.payload
        try:
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of amenities retrieved successfully')
    @api.marshal_list_with(amenity_response_model)
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    @api.marshal_with(amenity_response_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            return amenity.to_dict(), 200
        except ValueError:
            return {'message': 'Amenity not found'}, 404

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized')
    @api.marshal_with(amenity_response_model)
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        current_user = get_jwt_identity()
        user = facade.get_user(current_user)
        if not user.is_admin:
            return {'message': 'Admin privileges required'}, 403
        
        data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, data)
            return updated_amenity.to_dict(), 200
        except ValueError as e:
            if str(e) == "Amenity not found":
                return {'message': str(e)}, 404
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(204, 'Amenity deleted')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Unauthorized')
    def delete(self, amenity_id):
        """Delete an amenity (Admin only)"""
        current_user = get_jwt_identity()
        user = facade.get_user(current_user)
        if not user.is_admin:
            return {'message': 'Admin privileges required'}, 403
        
        try:
            facade.delete_amenity(amenity_id)
            return '', 204
        except ValueError as e:
            return {'message': str(e)}, 404
