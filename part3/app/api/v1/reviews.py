from flask import request, current_app
from flask_restx import Namespace, Resource, fields, marshal
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

# Définition du modèle de review (input validation et documentation)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'user_id': fields.String(required=False, description='ID of the user')
})

# Modèle pour les informations détaillées d'une review
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
    @api.response(403, 'Unauthorized action')
    def post(self):
        """Register a new review"""
        current_user = get_jwt_identity()
        try:
            review_data = request.get_json()
            if not review_data:
                return {"message": "Invalid input data: JSON required"}, 400
            
            review_data['user_id'] = current_user

            place = facade.get_place(review_data['place_id'])
            if not place:
                return {"message": "Place not found"}, 404
            
            if str(place.owner_id) == str(current_user):
                return {"message": "You cannot review your own place"}, 400

            existing_review = facade.get_review_by_user_and_place(current_user, review_data['place_id'])
            if existing_review:
                return {"message": "You have already reviewed this place"}, 400

            review = facade.create_review(review_data)
            return marshal(review, review_output_model), 201

        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            current_app.logger.error(f"Unexpected error in post review: {str(e)}")
            return {"message": "An unexpected error occurred"}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    @api.param('page', 'Page number', type=int, default=1)
    @api.param('per_page', 'Items per page', type=int, default=10)
    def get(self):
        """Retrieve a list of all reviews (Public)"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        reviews, total = facade.get_all_reviews(page=page, per_page=per_page)

        response_data = {
            'items': [marshal(review, review_output_model) for review in reviews],
            'total': total,
            'page': page,
            'per_page': per_page
        }

        return response_data, 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', review_output_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (Public)"""
        try:
            review = facade.get_review(review_id)
            
            if not review:
                return {"message": f"Review with ID {review_id} not found"}, 404
            
            return marshal(review, review_output_model), 200
        
        except Exception as e:
            current_app.logger.error(f"Unexpected error in get review: {str(e)}")
            return {"message": "An unexpected error occurred"}, 500

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully', review_output_model)
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    def put(self, review_id):
        """Update a review's information (Owner or Admin)"""
        current_user_claims = get_jwt()
        current_user_id = get_jwt_identity()
        try:
            review_data = request.get_json()
            if not review_data:
                return {"message": "Invalid input data: JSON required"}, 400
            
            review = facade.get_review(review_id)
            
            if not review:
                return {"message": f"Review with ID {review_id} not found"}, 404
            
            if not current_user_claims.get('is_admin', False) and str(review['user_id']) != str(current_user_id):
                return {"message": "Unauthorized action"}, 403

            updated_review = facade.update_review(review_id, review_data)

            return marshal(updated_review, review_output_model), 200
        
        except ValueError as e:
            return {"message": str(e)}, 400
        except Exception as e:
            current_app.logger.error(f"Unexpected error in put review: {str(e)}")
            return {"message": "An unexpected error occurred"}, 500

    @jwt_required()
    @api.response(204, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review (Owner or Admin)"""
        current_user_claims = get_jwt()
        current_user_id = get_jwt_identity()
        
        try:
            review = facade.get_review(review_id)
            
            if not review:
                return {"message": f"Review with ID {review_id} not found"}, 404
            
            if not current_user_claims.get('is_admin', False) and str(review['user_id']) != str(current_user_id):
                return {"message": "Unauthorized action"}, 403

            facade.delete_review(review_id)

            return '', 204
        
        except ValueError as e:
            return {"message": str(e)}, 400
