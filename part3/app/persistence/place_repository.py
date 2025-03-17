from app.models.place import Place
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    """Repository for the Place model"""

    def __init__(self):
        super().__init__(Place)
