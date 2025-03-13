from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declared_attr
from uuid import uuid4
from datetime import datetime
from app.extensions import db

class BaseModel:
    """Base class for all models"""
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initialize base model with common attributes"""
        if not 'id' in kwargs:
            self.id = str(uuid4())
        for key, value in kwargs.items():
            setattr(self, key, value)
        if not 'created_at' in kwargs:
            self.created_at = datetime.utcnow()
        if not 'updated_at' in kwargs:
            self.updated_at = self.created_at

    def to_dict(self):
        """Return dictionary of all instance attributes"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def save(self):
        """Update the updated_at attribute with current datetime and save to database"""
        self.updated_at = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
