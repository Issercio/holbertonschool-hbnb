from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship, joinedload
from .associations import place_amenity
import logging

class Place(BaseModel, db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(60), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")

    def __init__(self, title, owner_id, description="", price=0.0, latitude=0.0, longitude=0.0, **kwargs):
        super().__init__(**kwargs)
        self.validate_title(title)
        self.title = title
        self.owner_id = owner_id
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def validate_title(title):
        if not title:
            raise ValueError("Title cannot be empty")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or less")

    def to_dict(self):
        place_dict = super().to_dict()
        logging.debug(f"Converting place {self.id} to dict")
        logging.debug(f"Raw amenities for place {self.id}: {self.amenities}")
        
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'owner': {
                'id': self.owner.id,
                'first_name': self.owner.first_name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            } if self.owner else None
        })
        logging.debug(f"Amenities in place dict for {self.id}: {place_dict['amenities']}")
        return place_dict

    def __repr__(self):
        return f"<Place {self.title}>"
