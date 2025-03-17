from app.models.amenity import Amenity
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    """Repository for the Amenity model"""

    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name):
        """Retrieve an amenity by its name."""
        return self.model.query.filter_by(name=name).first()
