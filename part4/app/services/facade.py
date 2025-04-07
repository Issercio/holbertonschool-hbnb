from flask import current_app
from app.extensions import db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.persistence.user_repository import UserRepository
from abc import ABC, abstractmethod
from werkzeug.security import generate_password_hash

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

    def create_user(self, user_data):
        try:
            required_fields = ['first_name', 'last_name', 'email', 'password']
            for field in required_fields:
                if field not in user_data:
                    raise ValueError(f"Le champ {field} est obligatoire")

            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user:
                return existing_user

            user = self.user_repository.create_user({
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'password': generate_password_hash(user_data['password']),
                'is_admin': user_data.get('is_admin', False)
            })

            return user

        except Exception as e:
            current_app.logger.error(f"Erreur création utilisateur: {str(e)}")
            raise

    def get_users(self, page=None, per_page=None):
        users, total = self.user_repository.get_all(page, per_page)
        return [user.to_dict() for user in users], total

    def get_user(self, user_id):
        user = self.user_repository.get(user_id)
        return user

    def get_user_by_email(self, email):
        return self.user_repository.get_by_email(email)

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        if 'email' in user_data and user_data['email'] != user.email and self.get_user_by_email(user_data['email']):
            raise ValueError("Email already in use")
        
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password'])
        
        updated_user = self.user_repository.update(user_id, user_data)
        return updated_user

    def create_place(self, place_data):
        try:
            # Vérification de l'owner_id dans les données de place_data
            owner_email = place_data.get('owner_email')
            if not owner_email:
                raise ValueError("Owner email is required")

            owner = self.get_user_by_email(owner_email)
            if not owner:
                raise ValueError("Propriétaire invalide (owner_email).")

            # Ajout de l'owner_id dans les données de place_data
            place_data['owner_id'] = owner.id

            # Validation des autres champs
            price = float(place_data.get('price', 0.0))
            latitude = float(place_data.get('latitude', 0.0))
            longitude = float(place_data.get('longitude', 0.0))

            place = Place(
                title=place_data.get('title', ''),
                description=place_data.get('description', ''),
                price=price,
                latitude=latitude,
                longitude=longitude,
                owner_id=owner.id
            )

            # Ajout des amenities
            if 'amenities' in place_data:
                amenity_ids = place_data['amenities']
                if not isinstance(amenity_ids, list):
                    raise ValueError("Le champ 'amenities' doit être une liste d'identifiants.")

                for amenity_id in amenity_ids:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity invalide : {amenity_id}")
                    place.amenities.append(amenity)

            return self.place_repository.add(place)

        except ValueError as e:
            current_app.logger.error(f"Erreur lors de la création du lieu : {str(e)}")
            raise
        except Exception as e:
            current_app.logger.error(f"Erreur inattendue lors de la création du lieu : {str(e)}")
            raise ValueError(f"Une erreur inattendue s'est produite : {str(e)}")

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        return place

    def get_all_places(self, page=None, per_page=None):
        places, total = self.place_repository.get_all(page=page, per_page=per_page)
        
        formatted_places = []
        for place in places:
            place_dict = {
                'id': str(place.id) if place.id else None,
                'title': place.title if place.title else "",
                'description': place.description if place.description else "",
                'price': float(place.price) if place.price is not None else 0.0,
                'latitude': float(place.latitude) if place.latitude is not None else 0.0,
                'longitude': float(place.longitude) if place.longitude is not None else 0.0,
                'owner_id': str(place.owner_id) if place.owner_id else None,
                'created_at': place.created_at.isoformat() if place.created_at else None,
                'updated_at': place.updated_at.isoformat() if place.updated_at else None,
                'amenities': [{
                    'id': str(amenity.id) if amenity.id else None,
                    'name': amenity.name if amenity.name else None
                } for amenity in place.amenities] if place.amenities else [],
                'owner': {
                    'id': str(place.owner.id) if place.owner else None,
                    'first_name': place.owner.first_name if place.owner else None,
                    'last_name': place.owner.last_name if place.owner else None,
                    'email': place.owner.email if place.owner else None
                } if place.owner else None
            }
            formatted_places.append(place_dict)
        
        return formatted_places, total

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            
            if not isinstance(amenity_ids, list):
                raise ValueError("Le champ 'amenities' doit être une liste d'identifiants.")
            
            place.amenities.clear()
            
            for amenity_id in amenity_ids:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
                else:
                    current_app.logger.warning(f"Amenity with id {amenity_id} not found.")
        
        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)
        
        db.session.commit()
        return place

    def delete_place(self, place_id):
        return self.place_repository.delete(place_id)

    # Méthodes pour Reviews et Amenities
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
        return self.review_repository.add(review)

    def get_review(self, review_id):
        review = self.review_repository.get(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        return review

    def get_reviews_by_place(self, place_id):
        reviews = self.review_repository.get_by_place_id(place_id)
        return reviews

    def get_all_reviews(self, page=None, per_page=None):
        reviews, total = self.review_repository.get_all(page=page, per_page=per_page)
        formatted_reviews = [review.to_dict() for review in reviews]
        return formatted_reviews, total

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        updated_review = self.review_repository.update(review_id, review_data)
        return updated_review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            raise ValueError(f"Review with ID {review_id} not found")
        return self.review_repository.delete(review_id)

    def get_review_by_user_and_place(self, user_id, place_id):
        review = Review.query.filter_by(user_id=user_id, place_id=place_id).first()
        return review

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        return self.amenity_repository.add(amenity)

    def get_amenity(self, amenity_id):
        amenity = self.amenity_repository.get(amenity_id)
        return amenity

    def get_all_amenities(self, page=None, per_page=None):
        amenities, total = self.amenity_repository.get_all(page, per_page)
        return [amenity.to_dict() for amenity in amenities], total

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        updated_amenity = self.amenity_repository.update(amenity_id, amenity_data)
        return updated_amenity

    def delete_amenity(self, amenity_id):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        return self.amenity_repository.delete(amenity_id)
