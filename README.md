🏨 HBNB - Holberton AirBnB Clone
![Project Logo](https://via.placeholdere complet d'AirBnB construit avec Python et Flask.*

📋 Aperçu du projet
HBNB est une application robuste qui permet aux utilisateurs de :

S'inscrire et gérer leurs propriétés.

Laisser des avis.

Associer des commodités à des lieux.

🏗️ Architecture
Le projet suit une architecture en trois couches :

🖥️ Présentation : Interface API et web.

🧠 Logique métier : Modèles principaux et règles métier.

💾 Persistance : Interactions avec la base de données.

✨ Fonctionnalités
👤 Inscription et authentification des utilisateurs via JWT.

🏠 Gestion des propriétés (ajout, modification, suppression).

⭐ Système d'avis pour les propriétés.

🛋️ Gestion des commodités associées aux lieux.

👑 Fonctionnalités administratives.

📱 Interface web responsive.

📁 Structure du répertoire
text
.
├── app/
│   ├── api/
│   ├── models/
│   ├── persistence/
│   ├── services/
├── static/
├── templates/
├── tests/
├── config.py
├── run.py
└── setup.sql
🚀 Installation et configuration
Prérequis
🐍 Python 3.10+

🔄 Environnement virtuel (recommandé)

🗄️ SQLite ou MySQL

Étapes
Clonez le dépôt :

bash
git clone https://github.com/username/hbnb.git
cd hbnb
Créez un environnement virtuel :

bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
Installez les dépendances :

bash
pip install -r requirements.txt
Configurez la base de données :

bash
python setup.sql  # SQLite
Lancez l'application :

bash
python run.py
🌐 Endpoints API
🔐 Authentification
POST /api/v1/auth/login : Connexion utilisateur.

POST /api/v1/auth/register : Inscription utilisateur.

👤 Utilisateurs
GET /api/v1/users : Liste des utilisateurs.

🏠 Propriétés
GET /api/v1/places : Liste des propriétés.

⭐ Avis
POST /api/v1/places/<place_id>/reviews : Ajouter un avis.

🛋️ Commodités
GET /api/v1/amenities : Liste des commodités.

🖥️ Interface web
Accédez à l'application via ces pages :

/ : Page d'accueil.

/login : Connexion utilisateur.

/place/<place_id> : Détails d'une propriété.

📈 Évolution du projet
Le projet a évolué en plusieurs phases :

📝 Design de l'architecture.

🧠 Implémentation de la logique métier et API.

🔐 Intégration de l'authentification et base de données.

🎨 Développement de l'interface web.

🤝 Contribuer
Forkez le dépôt.

Créez une branche feature :

bash
git checkout -b feature/amazing-feature
Commitez vos modifications :

bash
git commit -m "Add amazing feature"
Poussez votre branche :

bash
git push origin feature/amazing-feature
Ouvrez une Pull Request.

📜 Licence
Ce projet est réalisé dans le cadre du programme éducatif de Holberton School.

🙏 Remerciements
Merci à :

🏫 Holberton School pour la structure du projet.

🌐 Les communautés Flask et SQLAlchemy pour leur documentation exceptionnelle.
