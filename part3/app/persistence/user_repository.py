from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.extensions import db
from sqlalchemy.exc import IntegrityError

class UserRepository(SQLAlchemyRepository):
    """Repository for the User model"""

    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        """Retrieve a user by their email."""
        return self.model.query.filter_by(email=email).first()

    def create_user(self, user_data):
        """Create a new user with validation and password hashing."""
        try:
            # Vérifier si l'email existe déjà
            if not User.check_email_uniqueness(user_data['email']):
                raise ValueError(f"Email {user_data['email']} already exists")

            # Créer l'utilisateur avec le modèle
            user = User(
                first_name=user_data.get('first_name', '').strip(),
                last_name=user_data.get('last_name', '').strip(),
                email=user_data.get('email', '').strip(),
                password=user_data['password'],
                is_admin=user_data.get('is_admin', False)
            )

            # Utiliser la méthode add() héritée de SQLAlchemyRepository
            self.add(user)
            
            # Retourner un dictionnaire complet de l'utilisateur
            return user.to_dict()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Database integrity error - email might be duplicate")

    def get_all(self, page=None, per_page=None):
        """Get all users with pagination."""
        query = self.model.query
        if page and per_page:
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)
            return pagination.items, pagination.total
        else:
            users = query.all()
            return users, len(users)

    def update(self, user_id, user_data):
        """Update a user."""
        user = self.get(user_id)
        if user:
            if 'email' in user_data and user_data['email'] != user.email:
                if not User.check_email_uniqueness(user_data['email']):
                    raise ValueError(f"Email {user_data['email']} already exists")
            for key, value in user_data.items():
                setattr(user, key, value)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                raise ValueError("Database integrity error - email might be duplicate")
            return user
        return None
