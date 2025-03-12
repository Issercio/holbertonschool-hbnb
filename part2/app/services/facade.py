from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from abc import ABC, abstractmethod
from datetime import datetime

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

class Facade:
    def __init__(self, use_db=True):
        if use_db:
            self.user_repository = SQLAlchemyRepository(User)
            self.place_repository = SQLAlchemyRepository(Place)
            self.amenity_repository = SQLAlchemyRepository(Amenity)
            self.review_repository = SQLAlchemyRepository(Review)
        else:
            # Implémentation pour InMemoryRepository si nécessaire
            pass

    def get_users(self):
        users = self.user_repository.get_all()
        return [user for user in users if not getattr(user, 'is_test_user', False)]

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def create_user(self, user_data):
        if not user_data.get('password'):
            raise ValueError("Password is required")
        
        # Vérifier si l'email existe déjà
        existing_user = self.user_repository.get_by_attribute('email', user_data['email'])
        if existing_user:
            raise ValueError(f"Email {user_data['email']} is already in use.")
        
        user = User(
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            email=user_data.get('email', ''),
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        
        return self.user_repository.add(user)

    def update_user(self, user_id, data):
        update_data = {k: v for k, v in data.items() if k in ['first_name', 'last_name', 'email'] and v is not None}
        return self.user_repository.update(user_id, update_data)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)
    
    # Méthodes pour les amenities
    def create_amenity(self, amenity_data):
        """Créer un nouvel amenity"""
        if not amenity_data.get('name'):
            raise ValueError("Name is required")
        
        amenity = Amenity(name=amenity_data.get('name'))
        return self.amenity_repository.add(amenity)

    def get_amenity(self, amenity_id):
        """Obtenir un amenity par son ID"""
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        """Obtenir tous les amenities"""
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Mettre à jour un amenity"""
        if 'name' in amenity_data and not amenity_data['name'].strip():
            raise ValueError("Name is required and cannot be empty")
            
        return self.amenity_repository.update(amenity_id, amenity_data)

    # Méthodes pour les places
    def create_place(self, place_data):
        """Créer un nouveau place"""
        # Validations
        if not place_data.get('title'):
            raise ValueError("Title is required")
        
        if len(place_data.get('title', '')) > 100:
            raise ValueError("Title must not exceed 100 characters")
            
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")
            
        owner = self.user_repository.get(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} does not exist")
            
        if 'price' in place_data and float(place_data.get('price', 0)) < 0:
            raise ValueError("Price cannot be negative")
            
        if 'latitude' in place_data and not -90 <= float(place_data.get('latitude', 0)) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        if 'longitude' in place_data and not -180 <= float(place_data.get('longitude', 0)) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        
        # Récupérer les amenities si spécifiés
        amenities = []
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repository.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
        
        # Créer le place
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=float(place_data.get('price', 0.0)),
            latitude=float(place_data.get('latitude', 0.0)),
            longitude=float(place_data.get('longitude', 0.0)),
            owner_id=owner_id,
            amenities=amenities
        )
        
        return self.place_repository.add(place)

    def get_place(self, place_id):
        """Obtenir un place par son ID"""
        return self.place_repository.get(place_id)

    def get_all_places(self):
        """Obtenir tous les places"""
        return self.place_repository.get_all()

    def get_places(self):
        """Alias pour get_all_places pour compatibilité"""
        return self.get_all_places()

    def update_place(self, place_id, place_data):
        """Mettre à jour un place"""
        # Validations
        if 'price' in place_data and float(place_data.get('price', 0)) < 0:
            raise ValueError("Price cannot be negative")
            
        if 'latitude' in place_data and not -90 <= float(place_data.get('latitude', 0)) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
            
        if 'longitude' in place_data and not -180 <= float(place_data.get('longitude', 0)) <= 180:
            raise ValueError("Longitude must be between -180 and 180")
            
        if 'owner_id' in place_data:
            owner = self.user_repository.get(place_data['owner_id'])
            if not owner:
                raise ValueError(f"Owner with ID {place_data['owner_id']} does not exist")
        
        # Gérer les amenities si nécessaire
        if 'amenities' in place_data:
            place = self.place_repository.get(place_id)
            if place:
                amenities = []
                for amenity_id in place_data['amenities']:
                    amenity = self.amenity_repository.get(amenity_id)
                    if amenity:
                        amenities.append(amenity)
                place_data['amenities'] = amenities
        
        return self.place_repository.update(place_id, place_data)

    def delete_place(self, place_id):
        """Supprimer un place"""
        return self.place_repository.delete(place_id)

    # Méthodes pour les reviews
    def create_review(self, review_data):
        """Créer une nouvelle review"""
        # Validations
        user_id = review_data.get('user_id')
        if not user_id or not self.user_repository.get(user_id):
            raise ValueError(f"User with ID {user_id} does not exist")
            
        place_id = review_data.get('place_id')
        if not place_id or not self.place_repository.get(place_id):
            raise ValueError(f"Place with ID {place_id} does not exist")
            
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
                review_data['rating'] = rating
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
                
        if not review_data.get('text'):
            raise ValueError("Review text is required")
            
        # Créer la review
        from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from abc import ABC, abstractmethod
from datetime import datetime


# Interface Repository
class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


# Implémentation InMemory
class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)


# Implémentation SQLAlchemy
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from abc import ABC, abstractmethod
from datetime import datetime

# Interface Repository
class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

# Implémentation InMemory
class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            return obj
        return None

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

# Implémentation SQLAlchemy
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

    def get_by_user_id(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def get_by_place_id(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()

# Façade
class Facade:
    def __init__(self, use_db=True):
        if use_db:
            self.user_repository = SQLAlchemyRepository(User)
            self.place_repository = SQLAlchemyRepository(Place)
            self.amenity_repository = SQLAlchemyRepository(Amenity)
            self.review_repository = SQLAlchemyRepository(Review)
        else:
            self.user_repository = InMemoryRepository()
            self.place_repository = InMemoryRepository()
            self.amenity_repository = InMemoryRepository()
            self.review_repository = InMemoryRepository()

    # Méthodes utilisateur
    def get_users(self):
        users = self.user_repository.get_all()
        return [user for user in users if not getattr(user, 'is_test_user', False)]

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def create_user(self, user_data):
        if not user_data.get('password'):
            raise ValueError("Password is required")
        
        user = User(
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            email=user_data.get('email', ''),
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        return self.user_repository.add(user)

    def update_user(self, user_id, data):
        update_data = {k: v for k, v in data.items() if k in ['first_name', 'last_name', 'email'] and v is not None}
        return self.user_repository.update(user_id, update_data)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

    # Méthodes pour les amenities
    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            raise ValueError("Name is required")
        amenity = Amenity(name=amenity_data.get('name'))
        return self.amenity_repository.add(amenity)

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        if 'name' in amenity_data and not amenity_data['name'].strip():
            raise ValueError("Name is required and cannot be empty")
        return self.amenity_repository.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)

    # Méthodes pour les places
    def create_place(self, place_data):
        self._validate_place_data(place_data)
        amenities = self._get_amenities_from_data(place_data)
        
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=float(place_data.get('price', 0.0)),
            latitude=float(place_data.get('latitude', 0.0)),
            longitude=float(place_data.get('longitude', 0.0)),
            owner_id=place_data.get('owner_id'),
            amenities=amenities
        )
        return self.place_repository.add(place)

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        self._validate_place_data(place_data, update=True)
        if 'amenities' in place_data:
            place_data['amenities'] = self._get_amenities_from_data(place_data)
        return self.place_repository.update(place_id, place_data)

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    # Méthodes pour les reviews
    def create_review(self, review_data):
        self._validate_review_data(review_data)
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            user_id=review_data.get('user_id'),
            place_id=review_data.get('place_id')
        )
        return self.review_repository.add(review)

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_by_place_id(place_id)

    def update_review(self, review_id, review_data):
        self._validate_review_data(review_data, update=True)
        return self.review_repository.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)

    # Méthodes de validation
    def _validate_place_data(self, place_data, update=False):
        if not update and not place_data.get('title'):
            raise ValueError("Title is required")
        if 'title' in place_data and len(place_data['title']) > 100:
            raise ValueError("Title must not exceed 100 characters")
        if not update and not place_data.get('owner_id'):
            raise ValueError("Owner ID is required")
        if 'owner_id' in place_data and not self.user_repository.get(place_data['owner_id']):
            raise ValueError(f"Owner with ID {place_data['owner_id']} does not exist")
        if 'price' in place_data and float(place_data['price']) < 0:
            raise ValueError("Price cannot be negative")
        if 'latitude' in place_data and not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if 'longitude' in place_data and not -180 <= float(place_data['longitude']) <= 180:
            from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from abc import ABC, abstractmethod
from datetime import datetime

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            return obj
        return None

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

    def get_by_user_id(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def get_by_place_id(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()

class Facade:
    def __init__(self, use_db=True):
        if use_db:
            self.user_repository = SQLAlchemyRepository(User)
            self.place_repository = SQLAlchemyRepository(Place)
            self.amenity_repository = SQLAlchemyRepository(Amenity)
            self.review_repository = SQLAlchemyRepository(Review)
        else:
            self.user_repository = InMemoryRepository()
            self.place_repository = InMemoryRepository()
            self.amenity_repository = InMemoryRepository()
            self.review_repository = InMemoryRepository()

    # User methods
    def get_users(self):
        users = self.user_repository.get_all()
        return [user for user in users if not getattr(user, 'is_test_user', False)]

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def create_user(self, user_data):
        if not user_data.get('password'):
            raise ValueError("Password is required")
        
        existing_user = self.user_repository.get_by_attribute('email', user_data['email'])
        if existing_user:
            raise ValueError(f"Email {user_data['email']} is already in use.")
        
        user = User(
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            email=user_data.get('email', ''),
            password=user_data['password'],
            is_admin=user_data.get('is_admin', False)
        )
        return self.user_repository.add(user)

    def update_user(self, user_id, data):
        update_data = {k: v for k, v in data.items() if k in ['first_name', 'last_name', 'email'] and v is not None}
        return self.user_repository.update(user_id, update_data)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

    # Amenity methods
    def create_amenity(self, amenity_data):
        if not amenity_data.get('name'):
            raise ValueError("Name is required")
        amenity = Amenity(name=amenity_data.get('name'))
        return self.amenity_repository.add(amenity)

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repository.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return amenity

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        if 'name' in amenity_data and not amenity_data['name'].strip():
            raise ValueError("Name is required and cannot be empty")
        return self.amenity_repository.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)

    # Place methods
    def create_place(self, place_data):
        self._validate_place_data(place_data)
        amenities = self._get_amenities_from_data(place_data)
        
        place = Place(
            title=place_data.get('title'),
            description=place_data.get('description', ''),
            price=float(place_data.get('price', 0.0)),
            latitude=float(place_data.get('latitude', 0.0)),
            longitude=float(place_data.get('longitude', 0.0)),
            owner_id=place_data.get('owner_id'),
            amenities=amenities
        )
        return self.place_repository.add(place)

    def get_place(self, place_id):
        return self.place_repository.get(place_id)

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        self._validate_place_data(place_data, update=True)
        if 'amenities' in place_data:
            place_data['amenities'] = self._get_amenities_from_data(place_data)
        return self.place_repository.update(place_id, place_data)

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    # Review methods
    def create_review(self, review_data):
        self._validate_review_data(review_data)
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            user_id=review_data.get('user_id'),
            place_id=review_data.get('place_id')
        )
        return self.review_repository.add(review)

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_by_place_id(place_id)

    def update_review(self, review_id, review_data):
        self._validate_review_data(review_data, update=True)
        return self.review_repository.update(review_id, review_data)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)

    # Validation methods
    def _validate_place_data(self, place_data, update=False):
        if not update and not place_data.get('title'):
            raise ValueError("Title is required")
        if 'title' in place_data and len(place_data['title']) > 100:
            raise ValueError("Title must not exceed 100 characters")
        if not update and not place_data.get('owner_id'):
            raise ValueError("Owner ID is required")
        if 'owner_id' in place_data and not self.user_repository.get(place_data['owner_id']):
            raise ValueError(f"Owner with ID {place_data['owner_id']} does not exist")
        if 'price' in place_data and float(place_data['price']) < 0:
            raise ValueError("Price cannot be negative")
        if 'latitude' in place_data and not -90 <= float(place_data['latitude']) <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if 'longitude' in place_data and not -180 <= float(place_data['longitude']) <= 180:
            raise ValueError("Longitude must be between -180 and 180")

    def _validate_review_data(self, review_data, update=False):
        if not update:
            if not review_data.get('user_id') or not self.user_repository.get(review_data['user_id']):
                raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
            if not review_data.get('place_id') or not self.place_repository.get(review_data['place_id']):
                raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")
        if 'rating' in review_data:
            try:
                rating = int(review_data['rating'])
                if not 1 <= rating <= 5:
                    raise ValueError("Rating must be between 1 and 5")
            except (ValueError, TypeError):
                raise ValueError("Rating must be an integer between 1 and 5")
        if not update and not review_data.get('text'):
            raise ValueError("Review text is required")

    def _get_amenities_from_data(self, data):
        amenities = []
        if 'amenities' in data and data['amenities']:
            for amenity_id in data['amenities']:
                amenity = self.amenity_repository.get(amenity_id)
                if amenity:
                    amenities.append(amenity)
        return amenities
