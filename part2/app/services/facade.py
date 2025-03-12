from app.models.place import Place
from app.models.user import User
from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
import logging

logging.basicConfig(level=logging.DEBUG)

class Facade:
    def __init__(self):
        """Initialiser les bases de données"""
        self.user_repository = SQLAlchemyRepository(User)
        self.place_repository = SQLAlchemyRepository(Place)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    # Méthodes utilisateur
    def get_users(self):
        """Obtenir tous les utilisateurs"""
        try:
            users = self.user_repository.get_all()
            return [user.to_dict() for user in users]
        except Exception as e:
            raise ValueError(f"Error getting users: {e}")

    def get_user(self, user_id):
        """Obtenir un utilisateur par ID"""
        try:
            user = self.user_repository.get(user_id)
            return user.to_dict() if user else None
        except NoResultFound:
            return None
        except Exception as e:
            raise ValueError(f"Error getting user: {e}")

    def get_user_by_email(self, email):
        """Obtenir un utilisateur par email"""
        try:
            user = self.user_repository.get_by_attribute('email', email)
            return user.to_dict() if user else None
        except Exception as e:
            raise ValueError(f"Error getting user by email: {e}")

    def create_user(self, user_data):
        """Créer un nouvel utilisateur"""
        try:
            existing_user = self.get_user_by_email(user_data.get('email'))
            if existing_user:
                raise ValueError("Un utilisateur avec cet email existe déjà")

            user = User(**user_data)
            created_user = self.user_repository.add(user)
            return created_user.to_dict()
        except IntegrityError:
            raise ValueError("Erreur d'intégrité lors de la création de l'utilisateur: données en double")
        except Exception as e:
            raise ValueError(f"Erreur lors de la création de l'utilisateur: {str(e)}")

    def update_user(self, user_id, data):
        """Mettre à jour un utilisateur existant"""
        try:
            user = self.user_repository.get(user_id)
            if not user:
                return None

            if 'email' in data:
                existing_user = self.get_user_by_email(data['email'])
                if existing_user and existing_user['id'] != user_id:
                    raise ValueError("Un autre utilisateur utilise déjà cet email")

            for key, value in data.items():
                setattr(user, key, value)

            updated_user = self.user_repository.add(user)  # Utiliser add pour mettre à jour
            return updated_user.to_dict()
        except IntegrityError:
            raise ValueError("Erreur d'intégrité lors de la mise à jour de l'utilisateur: données en double")
        except Exception as e:
            raise ValueError(f"Erreur lors de la mise à jour de l'utilisateur: {str(e)}")

    # Methods for places
    def get_places(self):
        """Obtenir tous les endroits"""
        try:
            # Charger les lieux avec leurs équipements et propriétaires
            places = self.place_repository.get_all(options=[joinedload(Place.amenities), joinedload(Place.owner)])
            logging.debug(f"Nombre de lieux récupérés : {len(places)}")

            # Construire la liste des lieux avec leurs équipements inclus
            result = []
            for place in places:
                logging.debug(f"Traitement du lieu : {place.id} - {place.title}")
                logging.debug(f"Nombre d'équipements pour ce lieu : {len(place.amenities)}")  # Log pour vérifier le nombre d'équipements
                for amenity in place.amenities:
                    logging.debug(f"Équipement trouvé : {amenity.id} - {amenity.name}")  # Log pour chaque équipement
                place_dict = place.to_dict()
                place_dict['amenities'] = [amenity.to_dict() for amenity in place.amenities]
                result.append(place_dict)

            return result
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des endroits : {str(e)}")
            raise ValueError(f"Erreur lors de la récupération des endroits : {str(e)}")

    def get_place(self, place_id):
        """Obtenir un endroit par ID"""
        try:
            # Charger un lieu spécifique avec ses équipements et son propriétaire
            place = self.place_repository.get(place_id, options=[joinedload(Place.amenities), joinedload(Place.owner)])
            if place:
                logging.debug(f"Lieu récupéré : {place.id} - {place.title}")
                logging.debug(f"Nombre d'équipements pour ce lieu : {len(place.amenities)}")  # Log pour vérifier le nombre d'équipements
                for amenity in place.amenities:
                    logging.debug(f"Équipement trouvé : {amenity.id} - {amenity.name}")  # Log pour chaque équipement
                place_dict = place.to_dict()
                place_dict['amenities'] = [amenity.to_dict() for amenity in place.amenities]
                return place_dict
            return None
        except Exception as e:
            logging.error(f"Erreur lors de la récupération du lieu : {str(e)}")
            raise ValueError(f"Erreur lors de la récupération du lieu : {str(e)}")

    def update_place(self, place_id, place_data):
        """Mettre à jour un endroit existant"""
        try:
            place = self.place_repository.get(place_id)
            if not place:
                return None

            for key, value in place_data.items():
                setattr(place, key, value)

            updated_place = self.place_repository.add(place)
            return updated_place.to_dict()
        except IntegrityError as e:
            logging.error(f"Erreur d'intégrité : {str(e)}")
            raise ValueError("Erreur d'intégrité lors de la mise à jour de l'endroit: données en double")
        except Exception as e:
            logging.error(f"Erreur inattendue : {str(e)}")
            raise ValueError(f"Erreur lors de la mise à jour de l'endroit: {str(e)}")

    def get_reviews_by_place(self, place_id):
        """Obtenir toutes les critiques pour un endroit spécifique"""
        try:
            place = self.place_repository.get(place_id)
            if not place:
                raise ValueError(f"Endroit {place_id} non trouvé")
            return [review.to_dict() for review in place.reviews]
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des critiques: {str(e)}")
            raise ValueError(f"Erreur lors de la récupération des critiques: {str(e)}")

    # Methods for amenities
    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        try:
            amenity = Amenity(**amenity_data)
            created_amenity = self.amenity_repository.add(amenity)
            return created_amenity.to_dict()
        except IntegrityError as e:
            logging.error(f"Erreur d'intégrité : {str(e)}")
            raise ValueError("Erreur d'intégrité lors de la création de l'équipement: données en double")
        except Exception as e:
            logging.error(f"Erreur inattendue : {str(e)}")
            raise ValueError(f"Error creating amenity: {e}")

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        try:
            amenity = self.amenity_repository.get(amenity_id)
            return amenity.to_dict() if amenity else None
        except NoResultFound as e:
            logging.error(f"Aucun équipement trouvé : {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de l'équipement : {str(e)}")
            raise ValueError(f"Error getting amenity: {e}")

    def get_all_amenities(self):
        """Get all amenities"""
        try:
            amenities = self.amenity_repository.get_all()
            return [amenity.to_dict() for amenity in amenities]
        except Exception as e:
            logging.error(f"Erreur lors de la récupération de tous les équipements : {str(e)}")
            raise ValueError(f"Error getting all amenities: {e}")

    def update_amenity(self, amenity_id, amenity_data):
        """Update an existing amenity"""
        try:
            amenity = self.amenity_repository.get(amenity_id)
            if not amenity:
                return None

            for key, value in amenity_data.items():
                setattr(amenity, key, value)

            updated_amenity = self.amenity_repository.add(amenity)  # Utiliser add pour mettre à jour
            return updated_amenity.to_dict()
        except IntegrityError as e:
            logging.error(f"Erreur d'intégrité : {str(e)}")
            raise ValueError("Erreur d'intégrité lors de la mise à jour de l'équipement: données en double")
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour de l'équipement: {str(e)}")
            raise ValueError(f"Erreur lors de la mise à jour de l'équipement: {str(e)}")
