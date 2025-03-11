from app.models import db
from app.models.base_model import BaseModel
import re

class User(BaseModel, db.Model):
    """Represents a user in the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a new User instance."""
        self.validate_first_name(first_name)
        self.validate_last_name(last_name)
        self.validate_email(email)

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @staticmethod
    def validate_first_name(first_name):
        """Validate first name."""
        if not first_name or first_name.strip() == "":
            raise ValueError("First name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("First name must be 50 characters or less")

    @staticmethod
    def validate_last_name(last_name):
        """Validate last name."""
        if not last_name or last_name.strip() == "":
            raise ValueError("Last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("Last name must be 50 characters or less")

    @staticmethod
    def validate_email(email):
        """Validate email format."""
        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")
        
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")

    def to_dict(self):
        """Convert user instance to dictionary representation."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'reviews': [review.id for review in self.reviews] if self.reviews else []
        }
