from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from .base_model import BaseModel
from app.extensions import bcrypt
from app.extensions import db
from app import bcrypt
import re

class User(BaseModel, db.Model):
    """Represents a user in the system."""
    
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)
    password = Column(String(60), nullable=False)

    reviews = relationship("Review", back_populates="user")

    def __init__(self, first_name, last_name, email, password, is_admin=False, **kwargs):
        """Initialize a new User instance."""
        super().__init__(**kwargs)
        
        self.validate_first_name(first_name)
        self.validate_last_name(last_name)
        self.validate_email(email)
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    @staticmethod
    def validate_first_name(first_name):
        if not first_name or len(first_name) > 50:
            raise ValueError("First name must be between 1 and 50 characters")

    @staticmethod
    def validate_last_name(last_name):
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name must be between 1 and 50 characters")

    @staticmethod
    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user instance to dictionary representation."""
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return user_dict

    @classmethod
    def create_user(cls, user_data):
        """Create a new user with validation"""
        try:
            user = cls(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password'],
                is_admin=user_data.get('is_admin', False)
            )
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise ValueError("Failed to create user: " + str(e))
        except KeyError as e:
            raise ValueError(f"Missing required field: {str(e)}")
