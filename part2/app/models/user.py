from app.extensions import db
from .base_model import BaseModel
import re
from sqlalchemy.orm import relationship

class User(BaseModel, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(60), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    places = relationship("Place", back_populates="owner", cascade="all, delete-orphan")

    def __init__(self, first_name, last_name, email, is_admin=False, **kwargs):
        super().__init__(**kwargs)
        self.validate_and_set_attributes(first_name, last_name, email, is_admin)

    def validate_and_set_attributes(self, first_name, last_name, email, is_admin):
        if not first_name or first_name.strip() == "":
            raise ValueError("First name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or less")
            
        if not last_name or last_name.strip() == "":
            raise ValueError("Last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or less")
            
        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")
        
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return user_dict

    def __repr__(self):
        return f"<User {self.email}>"
