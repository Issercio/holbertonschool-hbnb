from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review

class Facade:
    """
    Facade class to handle data operations using SQLAlchemy repositories.
    """
    def __init__(self):
        """Initialize repositories for different entities."""
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.amenity_repository = SQLAlchemyRepository(Amenity)
        self.review_repository = SQLAlchemyRepository(Review)

    # User-related methods
    def get_users(self):
        """Retrieve all users from the database."""
        return self.user_repository.get_all()

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repository.get(user_id)

    def create_user(self, user_data):
        """Create a new user in the database."""
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def update_user(self, user_id, data):
        """Update an existing user in the database."""
        user = self.get_user(user_id)
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            self.user_repository.add(user)  # Use add to persist changes
            return user
        return None

    def delete_user(self, user_id):
        """Delete a user from the database."""
        user = self.get_user(user_id)
        if user:
            self.user_repository.delete(user_id)
            return True
        return False

    # Amenity-related methods
    def create_amenity(self, amenity_data):
        """Create a new amenity in the database."""
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve an amenity by ID."""
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities from the database."""
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, data):
        """Update an existing amenity in the database."""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            for key, value in data.items():
                setattr(amenity, key, value)
            self.amenity_repository.add(amenity)  # Use add to persist changes
            return amenity
        return None

    def delete_amenity(self, amenity_id):
        """Delete an amenity from the database."""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            self.amenity_repository.delete(amenity_id)
            return True
        return False

    # Place-related methods
    def create_place(self, place_data):
        """Create a new place in the database."""
        place = Place(**place_data)
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repository.get(place_id)

    def get_all_places(self):
        """Retrieve all places from the database."""
        return self.place_repository.get_all()

    def update_place(self, place_id, data):
        """Update an existing place in the database."""
        place = self.get_place(place_id)
        if place:
            for key, value in data.items():
                setattr(place, key, value)
            self.place_repository.add(place)  # Use add to persist changes
            return place
        return None

    def delete_place(self, place_id):
        """Delete a place from the database."""
        place = self.get_place(place_id)
        if place:
            self.place_repository.delete(place_id)
            return True
        return False

    # Review-related methods
    def create_review(self, review_data):
        """Create a new review in the database."""
        review = Review(**review_data)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID."""
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews from the database."""
        return self.review_repository.get_all()

    def update_review(self, review_id, data):
        """Update an existing review in the database."""
        review = self.get_review(review_id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            self.review_repository.add(review)  # Use add to persist changes
            return review
        return None

    def delete_review(self, review_id):
        """Delete a review from the database."""
        review = self.get_review(review_id)
        if review:
            self.review_repository.delete(review_id)
            return True
        return False
