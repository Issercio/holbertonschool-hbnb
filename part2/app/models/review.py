from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from .base_model import BaseModel
from app.extensions import db
from .user import User
from .place import Place

class Review(BaseModel, db.Model):
    """Class representing a review"""
    
    __tablename__ = 'reviews'

    text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String, ForeignKey('places.id'), nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)

    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place, user, **kwargs):
        super().__init__(**kwargs)
        self.validate_text(text)
        self.validate_rating(rating)
        self.validate_relationships(place, user)

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @staticmethod
    def validate_text(text):
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating):
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    @staticmethod
    def validate_relationships(place, user):
        if not isinstance(place, Place):
            raise ValueError("Review must be associated with a valid Place")
        if not isinstance(user, User):
            raise ValueError("Review must be associated with a valid User")

    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place.id if self.place else None,
            'user_id': self.user.id if self.user else None
        })
        return review_dict

    @classmethod
    def create_review(cls, review_data):
        """Create a new review with validation"""
        try:
            # Text validation
            if not review_data.get('text'):
                raise ValueError("Review text cannot be empty")
            
            # Rating validation
            rating = review_data.get('rating')
            if rating is not None:
                try:
                    rating = int(rating)
                    if not 1 <= rating <= 5:
                        raise ValueError("Rating must be between 1 and 5")
                except (ValueError, TypeError):
                    raise ValueError("Rating must be an integer between 1 and 5")
            
            # User and Place validation
            place = Place.query.get(review_data['place_id'])
            user = User.query.get(review_data['user_id'])
            if not place:
                raise ValueError("Invalid place_id provided")
            if not user:
                raise ValueError("Invalid user_id provided")
            
            review = cls(
                text=review_data['text'],
                rating=rating,
                place=place,
                user=user
            )
            db.session.add(review)
            db.session.commit()
            return review
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Failed to create review: " + str(e))
