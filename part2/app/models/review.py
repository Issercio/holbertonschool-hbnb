from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(60), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place_id, user_id, **kwargs):
        super().__init__(**kwargs)
        self.validate_text(text)
        self.validate_rating(rating)
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @staticmethod
    def validate_text(text):
        if not text or not text.strip():
            raise ValueError("Review content cannot be empty")

    @staticmethod
    def validate_rating(rating):
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id
        })
        return review_dict

    def __repr__(self):
        return f"<Review {self.id}>"
