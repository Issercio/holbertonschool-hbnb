import os
from app import create_app
from config import config

# Déterminer l'environnement d'exécution
env = os.environ.get("FLASK_ENV", "development")

# Sélectionner la configuration appropriée
config_class = config.get(env, config['default'])

# Créer l'application
app = create_app(config_class)

if __name__ == '__main__':
    # Définir le mode debug en fonction de l'environnement
    debug = env == 'development'
    
    # Obtenir le port depuis les variables d'environnement ou utiliser 5000 par défaut
    port = int(os.environ.get("PORT", 5000))
    
    # Démarrer l'application
    app.run(host='0.0.0.0', port=port, debug=debug)
