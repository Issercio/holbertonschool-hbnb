from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Places management')

# Models for related entities (standardized names)
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(required=True, description='Amenity identifier'),
    'name': fields.String(required=True, description='Amenity name')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(required=True, description='User identifier'),
    'first_name': fields.String(required=True, description='Owner first name'),
    'last_name': fields.String(required=True, description='Owner last name'),
    'email': fields.String(required=True, description='Owner email')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(required=True, description='Review identifier'),
    'text': fields.String(required=True, description='Review content'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User identifier')
})

# Model for creating a place
place_model = api.model('Place', {
    'title': fields.String(
        required=True,
        description='Place title',
        min_length=1,
        max_length=100,
        example='Apartment with sea view'
    ),
    'owner_id': fields.String(
        required=True,
        description='Owner identifier',
        example='123e4567-e89b-12d3-a456-426614174000'
    ),
    'description': fields.String(
        required=False,
        description='Detailed place description',
        example='Beautiful apartment with sea view...'
    ),
    'price': fields.Float(
        required=True,
        description='Price per night (positive value)',
        example=120.50
    ),
    'latitude': fields.Float(
        required=False,
        description='Latitude (-90 to 90)',
        example=43.296482
    ),
    'longitude': fields.Float(
        required=False,
        description='Longitude (-180 to 180)',
        example=5.369780
    ),
    'amenities': fields.List(
        fields.String,
        required=False,
        description='List of amenity IDs',
        example=['123e4567-e89b-12d3-a456-426614174000']
    )
})

# Detailed place model
place_detail_model = api.model('PlaceDetail', {
    'id': fields.String(required=True, description='Place unique identifier'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Place latitude'),
    'longitude': fields.Float(description='Place longitude'),
    'owner': fields.Nested(user_model, required=True, description='Place owner'),
    'amenities': fields.List(fields.Nested(amenity_model), description='Available amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='Place reviews'),
    'created_at': fields.DateTime(required=True, description='Creation date'),
    'updated_at': fields.DateTime(required=True, description='Last update date')
})

# Model for creation/update response
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(required=True, description='Place unique identifier'),
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(description='Place latitude'),
    'longitude': fields.Float(description='Place longitude'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'owner': fields.Nested(user_model, required=True, description='Place owner'),
    'created_at': fields.DateTime(required=True, description='Creation date'),
    'updated_at': fields.DateTime(required=True, description='Last update date')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_response_model, mask=False)
    def get(self):
        """Get list of all places"""
        try:
            return facade.get_places()
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "Une erreur interne est survenue")

    @api.doc('create_place')
    @api.expect(place_model)
    @api.marshal_with(place_response_model, code=201, mask=False)
    @api.response(400, 'Validation Error')
    def post(self):
        """Create a new place"""
        try:
            return facade.create_place(api.payload), 201
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "Une erreur interne est survenue")

@api.route('/<string:place_id>')
@api.param('place_id', 'Unique identifier for the place')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_detail_model, mask=False)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            if place is None:
                api.abort(404, f"Place {place_id} not found")
            return place
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "Une erreur interne est survenue")

    @api.doc('update_place')
    @api.expect(place_model)
    @api.marshal_with(place_response_model, mask=False)
    @api.response(404, 'Place not found')
    @api.response(400, 'Validation Error')
    def put(self, place_id):
        """Update a place"""
        try:
            result = facade.update_place(place_id, api.payload)
            if result is None:
                api.abort(404, f"Place {place_id} not found")
            return result
        except ValueError as e:
            api.abort(400, str(e))
        except Exception as e:
            api.abort(500, "Une erreur interne est survenue")

@api.route('/<string:place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_list_with(review_model)
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return reviews
        except ValueError as e:
            api.abort(404, str(e))
        except Exception as e:
            api.abort(500, "Une erreur interne est survenue")
