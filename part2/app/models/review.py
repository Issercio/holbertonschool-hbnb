from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from .base_model import BaseModel
from app.extensions import db

class Review(BaseModel, db.Model):
    """Review model for property reviews"""
    
    __tablename__ = 'reviews'

    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Relations
    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place, user, **kwargs):
        """Initialize a new Review instance."""
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
        """Validate that the review text is not empty."""
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating):
        """Validate that the rating is an integer between 1 and 5."""
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    @staticmethod
    def validate_relationships(place, user):
        """Validate that the review is associated with valid Place and User instances."""
        from .place import Place
        from .user import User

        if not isinstance(place, Place):
            raise ValueError("Review must be associated with a valid Place")
        if not isinstance(user, User):
            raise ValueError("Review must be associated with a valid User")

    def to_dict(self):
        """Convert review instance to dictionary representation."""
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
        """Create a new review with validation."""
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
            from .place import Place
            from .user import User

            place = Place.query.get(review_data['place_id'])
            user = User.query.get(review_data['user_id'])
            if not place:
                raise ValueError("Invalid place_id provided")
            if not user:
                raise ValueError("Invalid user_id provided")
            
            # Create the review instance
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
