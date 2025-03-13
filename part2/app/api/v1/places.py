from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('places', description='Places management')

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity identifier'),
    'name': fields.String(description='Amenity name')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User identifier'),
    'first_name': fields.String(description='Owner first name'),
    'last_name': fields.String(description='Owner last name'),
    'email': fields.String(description='Owner email')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review identifier'),
    'text': fields.String(description='Review content'),
    'rating': fields.Integer(description='Rating (1-5)'),
    'user_id': fields.String(description='User identifier')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title', min_length=1, max_length=100),
    'owner_id': fields.String(required=False, description='Owner identifier'),
    'description': fields.String(required=False, description='Detailed place description'),
    'price': fields.Float(required=False, default=0.0, description='Price per night (positive value)'),
    'latitude': fields.Float(required=False, default=0.0, description='Latitude (-90 to 90)'),
    'longitude': fields.Float(required=False, default=0.0, description='Longitude (-180 to 180)'),
    'amenities': fields.List(fields.String, required=False, description='List of amenity IDs')
})

place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(description='Place unique identifier'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Place latitude'),
    'longitude': fields.Float(description='Place longitude'),
    'owner': fields.Nested(user_model, description='Place owner'),
    'amenities': fields.List(fields.Nested(amenity_model), description='Available amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='Place reviews'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place unique identifier'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Place latitude'),
    'longitude': fields.Float(description='Place longitude'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'owner': fields.Nested(user_model, description='Place owner'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model, mask=False)
    def get(self):
        """Get list of all places (Public)"""
        places, _ = facade.get_places()
        return [place.to_dict() for place in places]

    @jwt_required()
    @api.doc('create_place')
    @api.expect(place_model)
    @api.marshal_with(place_response_model, code=201, mask=False)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new place (Authenticated)"""
        current_user = get_jwt_identity()
        try:
            data = api.payload
            data['owner_id'] = current_user
            new_place = facade.create_place(data)
            return new_place.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, f"An internal error occurred: {str(e)}")

@api.route('/<string:place_id>')
@api.param('place_id', 'Unique identifier for the place')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_detail_model, mask=False)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (Public)"""
        place = facade.get_place(place_id)
        if place is None:
            api.abort(404, f"Place {place_id} not found")
        return place.to_dict()

    @jwt_required()
    @api.doc('update_place')
    @api.expect(place_model)
    @api.marshal_with(place_response_model, mask=False)
    @api.response(404, 'Place not found')
    @api.response(400, 'Validation Error')
    @api.response(403, 'Unauthorized action')
    def put(self, place_id):
        """Update a place (Owner or Admin)"""
        current_user = get_jwt()
        try:
            place = facade.get_place(place_id)
            if place is None:
                api.abort(404, f"Place {place_id} not found")
            if not current_user.get('is_admin', False) and place.owner_id != get_jwt_identity():
                api.abort(403, "Unauthorized action")
            updated_place = facade.update_place(place_id, api.payload, get_jwt_identity())
            return updated_place.to_dict()
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.doc('delete_place')
    @api.response(204, 'Place deleted')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """Delete a place (Owner or Admin)"""
        current_user = get_jwt()
        try:
            place = facade.get_place(place_id)
            if place is None:
                api.abort(404, f"Place {place_id} not found")
            if not current_user.get('is_admin', False) and place.owner_id != get_jwt_identity():
                api.abort(403, "Unauthorized action")
            facade.delete_place(place_id)
            return '', 204
        except ValueError as e:
            api.abort(400, str(e))

@api.route('/<string:place_id>/reviews')
@api.param('place_id', "The place's unique identifier")
class PlaceReviewList(Resource):
    @jwt_required()
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except ValueError as e:
            return {'message': str(e)}, 404
