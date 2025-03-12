from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model for detailed review information
review_output_model = api.model('ReviewOutput', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created', review_output_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        try:
            review_data = api.payload
            review = facade.create_review(review_data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_output_model)
    def get(self):
        """Retrieve a list of all reviews"""
        current_user = get_jwt_identity()
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @jwt_required()
    @api.response(200, 'Review details retrieved successfully', review_output_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        if review is None:
            api.abort(404, f"Review with ID {review_id} not found")
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully', review_output_model)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        try:
            review_data = api.payload
            updated_review = facade.update_review(review_id, review_data)
            if updated_review is None:
                api.abort(404, f"Review with ID {review_id} not found")
            return updated_review.to_dict(), 200
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        result = facade.delete_review(review_id)
        if not result:
            api.abort(404, f"Review with ID {review_id} not found")
        return {'message': 'Review deleted successfully'}, 200
