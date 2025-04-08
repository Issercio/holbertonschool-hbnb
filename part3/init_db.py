from app.extensions import db
from app.models.user import User
from app import create_app

def init_database():
    """Initialise la base de données en créant les tables."""
    app = create_app()
    with app.app_context():
        # Supprime toutes les tables existantes (facultatif)
        db.drop_all()
        print("Tables supprimées.")

        # Crée toutes les tables définies dans les modèles
        db.create_all()
        print("Tables créées.")

        # Ajoute des données initiales (exemple : utilisateur admin)
        create_admin_user()
        print("Données initiales ajoutées.")

def create_admin_user():
    """Crée un utilisateur administrateur par défaut."""
    admin_email = "admin@hbnb.io"
    admin_password = "admin1234"

    if not User.query.filter_by(email=admin_email).first():
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email=admin_email,
            password=admin_password,  # Ajout du mot de passe ici
            is_admin=True
        )
        admin_user.set_password(admin_password)  # Hachage du mot de passe

        db.session.add(admin_user)
        db.session.commit()
        print(f"Utilisateur administrateur créé : {admin_email}")
    else:
        print(f"L'utilisateur administrateur existe déjà : {admin_email}")


if __name__ == "__main__":
    init_database()
