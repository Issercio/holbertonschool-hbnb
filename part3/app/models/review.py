from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from .base_model import BaseModel
from app.extensions import db
from datetime import datetime

class Review(BaseModel, db.Model):
    """Class representing a review"""
    
    __tablename__ = 'reviews'

    # Colonnes de base
    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String, ForeignKey('places.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)

    # Relations (rétablies)
    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place_id=None, user_id=None, **kwargs):
        """Initialize a new Review instance."""
        super().__init__(**kwargs)
        self.validate_text(text)
        self.validate_rating(rating)

        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @staticmethod
    def validate_text(text):
        """Validate that the review text is not empty."""
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating):
        """Validate that the rating is an integer between 1 and 5."""
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        """Convert review instance to dictionary representation."""
        return {
            'id': str(self.id) if self.id else "",
            'text': self.text if self.text else "",
            'rating': self.rating if self.rating is not None else 0,
            'place_id': str(self.place_id) if self.place_id else "",
            'user_id': str(self.user_id) if self.user_id else "",
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else "",
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else ""
        }

    @classmethod
    def create_review(cls, review_data):
        """Create a new review with validation."""
        try:
            # Validate text
            if not review_data.get('text'):
                raise ValueError("Review text cannot be empty")
            
            # Validate rating
            rating = review_data.get('rating')
            if rating is not None:
                try:
                    rating = int(rating)
                    if not 1 <= rating <= 5:
                        raise ValueError("Rating must be between 1 and 5")
                except (ValueError, TypeError):
                    raise ValueError("Rating must be an integer between 1 and 5")
            
            # Validate User and Place relationships
            place_id = review_data.get('place_id')
            user_id = review_data.get('user_id')
            if not place_id:
                raise ValueError("Invalid place_id provided")
            if not user_id:
                raise ValueError("Invalid user_id provided")
            
            # Create the review instance
            review = cls(
                text=review_data['text'],
                rating=rating,
                place_id=place_id,
                user_id=user_id
            )
            
            db.session.add(review)
            db.session.commit()
            
            return review
        
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Failed to create review: " + str(e))
