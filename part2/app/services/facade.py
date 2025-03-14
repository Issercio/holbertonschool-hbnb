from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from abc import ABC, abstractmethod
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self, page=None, per_page=None):
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

    def get_all(self, page=None, per_page=None):
        if page and per_page:
            query = self.model.query.paginate(page=page, per_page=per_page)
            return query.items, query.total
        return self.model.query.all(), self.model.query.count()

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
    def __init__(self):
        self.user_repository = UserRepository()
        self.place_repository = SQLAlchemyRepository(Place)
        self.amenity_repository = SQLAlchemyRepository(Amenity)
        self.review_repository = SQLAlchemyRepository(Review)

    # User methods
    def get_users(self, page=None, per_page=None):
        users, total = self.user_repository.get_all(page, per_page)
        return [user.to_dict() for user in users], total

    def get_user(self, user_id):
        user = self.user_repository.get(user_id)
        return user.to_dict() if user else None

    def get_user_by_email(self, email):
        return self.user_repository.get_by_email(email)

    def create_user(self, user_data):
        return self.user_repository.create_user(user_data)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        if 'email' in user_data and user_data['email'] != user['email'] and self.get_user_by_email(user_data['email']):
            raise ValueError("Email already in use")
        
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password'])
        
        updated_user = self.user_repository.update(user_id, user_data)
        return updated_user.to_dict() if updated_user else None

    # Place methods
    def create_place(self, place_data):
        place = Place(**place_data)
        return self.place_repository.add(place).to_dict()

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        return place.to_dict() if place else None

    def get_places(self, page=None, per_page=None):
        places, total = self.place_repository.get_all(page, per_page)
        return [place.to_dict() for place in places], total

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        updated_place = self.place_repository.update(place_id, place_data)
        return updated_place.to_dict() if updated_place else None

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    # Review methods
    def create_review(self, review_data):
        existing_review = self.get_review_by_user_and_place(review_data['user_id'], review_data['place_id'])
        if existing_review:
            raise ValueError("User has already reviewed this place")

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Invalid place_id provided")

        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("Invalid user_id provided")

        review = Review(**review_data)
        return self.review_repository.add(review).to_dict()

    def get_review(self, review_id):
        review = self.review_repository.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        return review.to_dict()

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repository.get_by_place_id(place_id)
        return [review.to_dict() for review in reviews]

    def get_all_reviews(self, page=None, per_page=None):
        reviews, total = self.review_repository.get_all(page, per_page)
        return [review.to_dict() for review in reviews], total

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        updated_review = self.review_repository.update(review_id, review_data)
        return updated_review.to_dict() if updated_review else None

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        return self.review_repository.delete(review_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        review = Review.query.filter_by(user_id=user_id, place_id=place_id).first()
        return review.to_dict() if review else None

    # Amenity methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        return self.amenity_repository.add(amenity).to_dict()

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repository.get(amenity_id)
        return amenity.to_dict() if amenity else None

    def get_all_amenities(self):
        amenities, _ = self.amenity_repository.get_all()
        return [amenity.to_dict() for amenity in amenities]

    def update_amenity(self, amenity_id, amenity_data):
        updated_amenity = self.amenity_repository.update(amenity_id, amenity_data)
        return updated_amenity.to_dict() if updated_amenity else None
