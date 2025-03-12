from abc import ABC, abstractmethod
from app.extensions import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import joinedload
import logging

class Repository(ABC):
    """Abstract base class defining the interface for data persistence operations."""
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id, options=None):
        pass

    @abstractmethod
    def get_all(self, options=None):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value, options=None):
        pass

class InMemoryRepository(Repository):
    """In-memory implementation of the Repository interface."""
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id, options=None):
        return self._storage.get(obj_id)

    def get_all(self, options=None):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value, options=None):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Duplicate entry or integrity constraint violated")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise ValueError(f"Error adding object: {str(e)}")

    def get(self, obj_id, options=None):
        query = self.model.query
        if options:
            for option in options:
                query = query.options(option)
        return query.get(obj_id)

    def get_all(self, options=None):
        query = self.model.query
        if options:
            for option in options:
                query = query.options(option)
        
        logging.debug(f"Executing get_all for {self.model.__name__}")
        logging.debug(f"Query options: {options}")
        
        results = query.all()
        
        logging.debug(f"Number of {self.model.__name__} objects retrieved: {len(results)}")
        for obj in results:
            if hasattr(obj, 'amenities'):
                logging.debug(f"{self.model.__name__} {obj.id} has {len(obj.amenities)} amenities")
        
        return results

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            try:
                for key, value in data.items():
                    setattr(obj, key, value)
                db.session.commit()
                return obj
            except IntegrityError:
                db.session.rollback()
                raise ValueError("Duplicate entry or integrity constraint violated")
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ValueError(f"Error updating object: {str(e)}")
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            try:
                db.session.delete(obj)
                db.session.commit()
                return True
            except SQLAlchemyError as e:
                db.session.rollback()
                raise ValueError(f"Error deleting object: {str(e)}")
        return False

    def get_by_attribute(self, attr_name, attr_value, options=None):
        query = self.model.query.filter(getattr(self.model, attr_name) == attr_value)
        if options:
            for option in options:
                query = query.options(option)
        return query.first()
