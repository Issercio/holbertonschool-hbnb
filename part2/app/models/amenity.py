from app.models import db
from app.models.base_model import BaseModel

class Amenity(BaseModel, db.Model):
    """Class representing an amenity."""
    __tablename__ = 'amenities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name: str):
        """
        Initialize a new amenity.
        Args:
            name (str): Name of the amenity.
        """
        super().__init__()
        self.name = name

    def to_dict(self):
        """Convert amenity to dictionary."""
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'id': self.id,
            'name': self.name
        })
        return amenity_dict
