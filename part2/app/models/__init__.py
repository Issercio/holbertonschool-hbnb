from flask_sqlalchemy import SQLAlchemy

# Initialisation de l'instance SQLAlchemy
db = SQLAlchemy()

# Importation des modèles pour qu'ils soient enregistrés avec SQLAlchemy
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
