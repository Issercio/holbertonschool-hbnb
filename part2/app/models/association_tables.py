from app.extensions import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id', name='fk_place_amenity_place'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id', name='fk_place_amenity_amenity'), primary_key=True),
    db.UniqueConstraint('place_id', 'amenity_id', name='uq_place_amenity')
)
