from sqlalchemy import Column, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from app.extensions import db
from .association_tables import place_amenity  # Import de la table d'association

class Place(BaseModel, db.Model):
    """Class representing a rental place"""
    
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0.0)
    latitude = Column(Float)
    longitude = Column(Float)
    owner_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="places")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")  # Utilisation de la table d'association
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")

    def __init__(self, title, owner, description="", price=0.0, latitude=0.0, longitude=0.0, **kwargs):
        super().__init__(**kwargs)
        self.validate_title(title)
        self.validate_owner(owner)
        self.title = title
        self.owner = owner
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    @staticmethod
    def validate_title(title):
        if not title or len(title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")

    @staticmethod
    def validate_owner(owner):
        from .user import User
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User instance")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not -90 <= float(value) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not -180 <= float(value) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def to_dict(self):
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if self.owner else None,
            'amenities': [amenity.id for amenity in self.amenities] if self.amenities else []
        })
        return place_dict
