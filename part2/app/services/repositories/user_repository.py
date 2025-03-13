from app.models.user import User
from app import db
from app.services.repositories.repository_base import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email):
        """Get a user by their email address"""
        return self.model.query.filter_by(email=email).first()
    
    def update(self, user_id, data):
        """Update user with additional email uniqueness check"""
        user = self.get(user_id)
        if not user:
            return None
            
        if 'email' in data:
            existing_user = self.get_by_email(data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already in use")
        
        for key, value in data.items():
            setattr(user, key, value)
        
        db.session.commit()
        return user
