from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Modèle pour valider les données d'entrée de connexion
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Success')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authentifier l'utilisateur et retourner un token JWT"""
        credentials = api.payload
        
        try:
            # Étape 1 : Récupérer l'utilisateur par email
            user = facade.get_user_by_email(credentials['email'])
            
            # Étape 2 : Vérifier si l'utilisateur existe et si le mot de passe est correct
            if not user or not user.verify_password(credentials['password']):
                return {'error': 'Invalid credentials'}, 401

            # Étape 3 : Créer un token JWT avec l'ID utilisateur et le rôle admin
            access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
            
            # Étape 4 : Retourner le token JWT au client
            return {'access_token': access_token}, 200
        
        except Exception as e:
            return {'error': str(e)}, 500
