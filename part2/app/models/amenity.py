from app.extensions import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship
from .associations import place_amenity
import logging

class Amenity(BaseModel, db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(60), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    places = relationship("Place", secondary=place_amenity, back_populates="amenities")

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.validate_name(name)
        self.name = name

    @staticmethod
    def validate_name(name: str):
        if not name or len(name) > 50:
            raise ValueError("Amenity name must be between 1 and 50 characters")

    def to_dict(self):
        logging.debug(f"Converting amenity {self.id} to dict")
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name,
            'places': [place.id for place in self.places] if self.places else []
        })
        logging.debug(f"Amenity dict for {self.id}: {amenity_dict}")
        return amenity_dict

    def __repr__(self):
        return f"<Amenity {self.name}>"
