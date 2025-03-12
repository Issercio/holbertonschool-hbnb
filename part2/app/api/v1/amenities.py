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
    def post(self):
        """Register a new amenity"""
        current_user = get_jwt_identity()
        data = api.payload
        try:
            # Use the facade to create a new amenity
            amenity = facade.create_amenity(data)
            return amenity.to_dict(), 201  # Ensure the response is serialized properly
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        current_user = get_jwt_identity()
        amenities = facade.get_all_amenities()
        # Serialize each amenity to a dictionary for JSON response
        return [amenity.to_dict() for amenity in amenities], 200


@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @jwt_required()
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        current_user = get_jwt_identity()
        try:
            # Use the facade to retrieve the amenity
            amenity = facade.get_amenity(amenity_id)
            return amenity.to_dict(), 200  # Serialize the response
        except ValueError:
            return {'message': 'Amenity not found'}, 404

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        current_user = get_jwt_identity()
        data = api.payload
        try:
            # Use the facade to update the amenity
            updated_amenity = facade.update_amenity(amenity_id, data)
            return updated_amenity.to_dict(), 200  # Serialize the response
        except ValueError as e:
            if str(e) == "Amenity not found":
                return {'message': str(e)}, 404
            return {'message': str(e)}, 400
