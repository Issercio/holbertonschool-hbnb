from app.models import db
from app.models.base_model import BaseModel

class Place(BaseModel, db.Model):
    """Class representing a rental place."""
    __tablename__ = 'places'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationships
    amenities = db.relationship('Amenity', secondary='place_amenities', backref='places')
    reviews = db.relationship('Review', backref='place', lazy=True)

    def __init__(self, title, owner_id, description="", price=0.0, latitude=None, longitude=None):
        """
        Initialize a new Place.
        
        Args:
            title (str): Place title (required).
            owner_id (int): ID of the user who owns the place.
            description (str): Detailed description of the place.
            price (float): Price per night.
            latitude (float): Geographic latitude.
            longitude (float): Geographic longitude.
        """
        self.title = title
        self.owner_id = owner_id
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        """Convert place to dictionary."""
        place_dict = super().to_dict()
        place_dict.update({
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'amenities': [amenity.id for amenity in self.amenities] if self.amenities else [],
            'reviews': [review.id for review in self.reviews] if self.reviews else []
        })
        return place_dict
