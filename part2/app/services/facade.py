from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.repositories.repository_base import SQLAlchemyRepository, InMemoryRepository
from app.services.repositories.user_repository import UserRepository

class Facade:
    def __init__(self, use_db=True):
        if use_db:
            self.user_repository = UserRepository()
            self.place_repository = SQLAlchemyRepository(Place)
            self.amenity_repository = SQLAlchemyRepository(Amenity)
            self.review_repository = SQLAlchemyRepository(Review)
        else:
            self.user_repository = InMemoryRepository()
            self.place_repository = InMemoryRepository()
            self.amenity_repository = InMemoryRepository()
            self.review_repository = InMemoryRepository()

    # Méthodes utilisateur
    def get_users(self, page=None, per_page=None):
        users, total = self.user_repository.get_all(page=page, per_page=per_page)
        return [user for user in users if not getattr(user, 'is_test_user', False)], total

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def create_user(self, user_data):
        if not user_data.get('password'):
            raise ValueError("Password is required")
        
        user = User(
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            email=user_data.get('email', ''),
            password=generate_password_hash(user_data['password']),
            is_admin=user_data.get('is_admin', False)
        )
        return self.user_repository.add(user)

    def update_user(self, user_id, data):
        # Prevent email and password modification
        if 'email' in data or 'password' in data:
            raise ValueError("Email and password cannot be updated through this method.")
            
        update_data = {k: v for k, v in data.items() if k in ['first_name', 'last_name'] and v is not None}
        return self.user_repository.update(user_id, update_data)

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

    def change_user_password(self, user_id, current_password, new_password):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        if not check_password_hash(user.password, current_password):
            raise ValueError("Invalid current password")
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return True

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

    def get_places(self):
        return self.get_all_places()

    def update_place(self, place_id, place_data, current_user_id):
        place = self.get_place(place_id)
        if not place:
            raise ValueError(f"Place with ID {place_id} not found")
            
        if place.owner_id != current_user_id:
            raise ValueError("You are not authorized to update this place")
        
        self._validate_place_data(place_data, update=True)
        if 'amenities' in place_data:
            place_data['amenities'] = self._get_amenities_from_data(place_data)
        return self.place_repository.update(place_id, place_data)

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    # Méthodes pour les reviews
    def create_review(self, review_data):
        self._validate_review_data(review_data)

        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        # Vérifier si l'utilisateur est le propriétaire du lieu
        place = self.get_place(place_id)
        if place.owner_id == user_id:
            raise ValueError("You cannot review your own place")
        
        # Vérifier si l'utilisateur a déjà commenté ce lieu
        existing_review = self.review_repository.get_by_attribute('user_id', user_id)
        if existing_review and existing_review.place_id == place_id:
            raise ValueError("You have already reviewed this place")
        
        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            user_id=user_id,
            place_id=place_id
        )
        return self.review_repository.add(review)

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_by_place_id(place_id)

    def get_all_reviews(self, page=None, per_page=None):
         reviews, total =  self.review_repository.get_all(page=page, per_page=per_page)
         return reviews, total

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
