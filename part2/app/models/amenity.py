# models/amenity.py
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel
from app.extensions import db
from .association_tables import place_amenity

class Amenity(BaseModel, db.Model):
    """Amenity model for property features"""
    
    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)
    
    # Relation many-to-many avec Place
    places = relationship("Place", secondary=place_amenity, back_populates="amenities")
