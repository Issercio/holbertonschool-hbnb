from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from abc import ABC, abstractmethod
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

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
        self._commit()
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
            self._commit()
            return obj
        return None

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            self._commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()

    def get_by_user_id(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def get_by_place_id(self, place_id):
        return self.model.query.filter_by(place_id=place_id).all()

    def _commit(self):
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

class Facade:
    def __init__(self):
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.amenity_repository = SQLAlchemyRepository(Amenity)
        self.review_repository = SQLAlchemyRepository(Review)

    def create_user(self, first_name, last_name, email, password, is_admin=False):
        try:
            user = User.create_user(first_name, last_name, email, password, is_admin)
            return user
        except ValueError as e:
            raise ValueError(str(e))

    def get_users(self, page=None, per_page=None):
        users, total = self.user_repository.get_all(page, per_page)
        return [user.to_dict() for user in users], total

    def get_user(self, user_id):
        user = self.user_repository.get(user_id)
        return user

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        if 'email' in user_data and user_data['email'] != user.email and self.get_user_by_email(user_data['email']):
            raise ValueError("Email already in use")

        for key, value in user_data.items():
            setattr(user, key, value)

        db.session.commit()
        return user

    def create_place(self, title, description, price, latitude, longitude, owner_email, amenity_ids=None):
        try:
            owner = self.get_user_by_email(owner_email)
            if not owner:
                raise ValueError("Invalid owner email.")

            place = Place(
                title=title,
                description=description,
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=owner.id
            )

            if amenity_ids:
                for amenity_id in amenity_ids:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity with id {amenity_id} not found.")
                    place.amenities.append(amenity)

            db.session.add(place)
            db.session.commit()
            return place
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e))

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        return place

    def get_all_places(self, page=None, per_page=None):
        places, total = self.place_repository.get_all(page, per_page)
        return [{
            'id': str(p.id),
            'title': p.title,
            'description': p.description,
            'price': float(p.price),
            'latitude': float(p.latitude),
            'longitude': float(p.longitude),
            'owner_id': str(p.owner_id),
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'updated_at': p.updated_at.isoformat() if p.updated_at else None,
            'amenities': [{'id': str(a.id), 'name': a.name} for a in p.amenities],
            'owner': {
                'id': str(p.owner.id),
                'first_name': p.owner.first_name,
                'last_name': p.owner.last_name,
                'email': p.owner.email
            } if p.owner else None
        } for p in places], total

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")

        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            place.amenities.clear()

            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with id {amenity_id} not found.")
                place.amenities.append(amenity)

        for key, value in place_data.items():
            setattr(place, key, value)

        db.session.commit()
        return place

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    def create_review(self, user_id, place_id, text, rating):
        try:
            user = self.get_user(user_id)
            if not user:
                raise ValueError("Invalid user_id provided")

            place = self.get_place(place_id)
            if not place:
                raise ValueError("Invalid place_id provided")

            review = Review(user_id=user_id, place_id=place_id, text=text, rating=rating)
            db.session.add(review)
            db.session.commit()
            return review
        except Exception as e:
            db.session.rollback()
            raise ValueError(str(e))

    def get_review(self, review_id):
        review = self.review_repository.get(review_id)
        return review

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repository.get_by_place_id(place_id)
        return reviews

    def get_all_reviews(self, page=None, per_page=None):
        reviews, total = self.review_repository.get_all(page, per_page)
        return [{
            'id': str(r.id),
            'user_id': str(r.user_id),
            'place_id': str(r.place_id),
            'text': r.text,
            'rating': r.rating
        } for r in reviews], total

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError("Review not found")

        for key, value in review_data.items():
            setattr(review, key, value)

        db.session.commit()
        return review

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        return Review.query.filter_by(user_id=user_id, place_id=place_id).first()

    def create_amenity(self, name):
        amenity = Amenity(name=name)
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repository.get(amenity_id)
        return amenity

    def get_all_amenities(self, page=None, per_page=None):
        amenities, total = self.amenity_repository.get_all(page, per_page)
        return [{
            'id': str(a.id),
            'name': a.name
        } for a in amenities], total

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        for key, value in amenity_data.items():
            setattr(amenity, key, value)

        db.session.commit()
        return amenity

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)
