from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from app.extensions import db
from .association_tables import place_amenity

class Place(BaseModel, db.Model):
    """Class representing a rental place"""
    
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(String, default="")
    price = Column(Float, default=0.0)
    latitude = Column(Float, default=0.0)
    longitude = Column(Float, default=0.0)

    # Relations (rétablies)
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", back_populates="places")
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")
    reviews = relationship("Review", back_populates="place")

    def __init__(self, title, description="", price=0.0, latitude=0.0, longitude=0.0, owner_id=None, **kwargs):
        """Initialize a new Place instance."""
        super().__init__(**kwargs)
        self.validate_title(title)
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

    @staticmethod
    def validate_title(title):
        """Validate that the title is not empty and less than 100 characters."""
        if not title or len(title) > 100:
            raise ValueError("Title must be between 1 and 100 characters")

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        """Validate that the price is non-negative."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Validate that the latitude is between -90 and 90."""
        if not isinstance(value, (int, float)) or not -90 <= float(value) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Validate that the longitude is between -180 and 180."""
        if not isinstance(value, (int, float)) or not -180 <= float(value) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def to_dict(self):
        """Convert place instance to dictionary representation."""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [amenity.id for amenity in self.amenities] if self.amenities else []
        })
        return place_dict
