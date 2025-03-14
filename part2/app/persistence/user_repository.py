from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    """Repository for the User model"""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        """Retrieve a user by their email."""
        return self.model.query.filter_by(email=email).first()
