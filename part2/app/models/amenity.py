# models/amenity.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from app.extensions import db
from .association_tables import place_amenity  # Importez la table d'association

class Amenity(BaseModel, db.Model):
    """Class representing an amenity in the system."""

    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)
    places = relationship('Place', secondary=place_amenity, back_populates='amenities')  # Utilisez la table d'association importée

    def __init__(self, name: str):
        """
        Initialize a new amenity.
        
        Args:
            name (str): Name of the amenity
        """
        super().__init__()
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name: str):
        """
        Validate the amenity name.
        
        Args:
            name (str): Name to validate
        
        Raises:
            ValueError: If the name is invalid
        """
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters")

    def add_place(self, place):
        """
        Add a place to the amenity.
        
        Args:
            place (Place): Place object to add
        """
        if place not in self.places:
            self.places.append(place)

    def to_dict(self):
        """
        Convert amenity to dictionary representation.
        
        Returns:
            dict: Dictionary representation of the amenity
        """
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict
