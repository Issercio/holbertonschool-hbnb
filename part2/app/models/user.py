from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.exc import IntegrityError
from .base_model import BaseModel
from app.extensions import bcrypt, db
import re

class User(BaseModel, db.Model):
    """Represents a user in the system."""
    
    __tablename__ = 'users'

    # Columns
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)  # Contrainte UNIQUE
    is_admin = Column(Boolean, default=False)
    password = Column(String(60), nullable=False)

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
        self.hash_password(password)

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
        """
        Create a new user with validation.
        
        Args:
            user_data (dict): Data for creating a new user.
        
        Returns:
            User: The created user object.
        
        Raises:
            ValueError: If the email already exists or other validation fails.
        """
        try:
            # Vérifier si l'email existe déjà dans la base de données
            existing_user = cls.query.filter_by(email=user_data['email']).first()
            if existing_user:
                raise ValueError(f"Email {user_data['email']} is already in use.")

            # Créer un nouvel utilisateur après validation des données
            user = cls(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password'],  # Le mot de passe sera hashé dans le modèle
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

    @classmethod
    def get_by_email(cls, email):
        """
        Retrieve a user by their email.
        
        Args:
            email (str): The email of the user to retrieve.
        
        Returns:
            User: The user object if found, None otherwise.
        """
        return cls.query.filter_by(email=email).first()
