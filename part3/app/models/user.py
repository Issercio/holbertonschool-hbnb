import re
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship
from app.extensions import bcrypt, db
from .base_model import BaseModel

class User(BaseModel):
    """Represents a user in the system."""
    
    __tablename__ = 'users'

    # Colonnes
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128), nullable=False)

    # Relations
    reviews = relationship("Review", back_populates="user")
    places = relationship("Place", back_populates="owner")

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
        self.set_password(password)

    @staticmethod
    def validate_first_name(first_name):
        """Validate the first name."""
        if not first_name or len(first_name) > 50:
            raise ValueError("First name must be between 1 and 50 characters")

    @staticmethod
    def validate_last_name(last_name):
        """Validate the last name."""
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name must be between 1 and 50 characters")

    @staticmethod
    def validate_email(email):
        """Validate the email format."""
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

    def set_password(self, password: str):
        """
        Hashes and sets the password.
        
        Args:
            password (str): The plain-text password to hash.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the hashed password.
        
        Args:
            password (str): The plain-text password to verify.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Convert user instance to dictionary representation."""
        return {
            'id': self.id or '',
            'first_name': self.first_name or '',
            'last_name': self.last_name or '',
            'email': self.email or '',
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def check_email_uniqueness(cls, email):
        """Vérifie si l'email existe déjà"""
        return cls.query.filter_by(email=email).first() is None
