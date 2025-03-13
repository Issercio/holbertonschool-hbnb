from sqlalchemy import Table, Column, ForeignKey, String
from app.extensions import db

place_amenity = Table('place_amenity', db.Model.metadata,
    Column('place_id', String, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String, ForeignKey('amenities.id'), primary_key=True)
)
