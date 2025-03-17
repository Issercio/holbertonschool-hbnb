from app.models.review import Review
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    """Repository for the Review model"""

    def __init__(self):
        super().__init__(Review)
