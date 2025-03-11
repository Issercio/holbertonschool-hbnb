from app.models import db
from app.models.base_model import BaseModel
from datetime import datetime

class Review(BaseModel, db.Model):
    """Class representing a review"""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, text, rating, place_id, user_id):
        """Initialize a new review"""
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @staticmethod
    def validate_text(text):
        """Validate review content"""
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating):
        """Validate rating"""
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def create_review(cls, review_data):
        """Create a new review with validation"""
        cls.validate_text(review_data.get('text'))
        cls.validate_rating(review_data.get('rating'))

        new_review = cls(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict()
