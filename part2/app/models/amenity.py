# models/amenity.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from app.extensions import db

class Amenity(BaseModel, db.Model):
    """Class representing an amenity"""

    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)
    places = relationship('Place', secondary='place_amenity', back_populates='amenities')

    def __init__(self, name: str):
        """
        Initialize a new amenity
        Args:
            name (str): Name of the amenity
        """
        super().__init__()
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name: str):
        """Validate amenity name"""
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters")

    def add_place(self, place):
        """Add a place to the amenity"""
        if place not in self.places:
            self.places.append(place)

    def to_dict(self):
        """Convert amenity to dictionary"""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict
