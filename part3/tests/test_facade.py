import unittest
from unittest.mock import Mock, patch
from app import create_app
from app.services.facade import Facade
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestFacade(unittest.TestCase):

    def setUp(self):
        """
        Configure l'application Flask pour les tests.
        Crée un contexte d'application pour chaque test.
        """
        self.app = create_app('config.TestingConfig')  # Utilise la configuration de test
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.facade = Facade()

    def tearDown(self):
        """
        Supprime le contexte de l'application après chaque test.
        """
        self.app_context.pop()

    @patch('app.persistence.user_repository.UserRepository')
    def test_get_users(self, mock_user_repo):
        """
        Teste la méthode get_users de la façade.
        Vérifie que les utilisateurs sont correctement récupérés.
        """
        mock_user = Mock(spec=User)
        mock_user.to_dict.return_value = {'id': '1', 'name': 'Test User'}
        mock_user_repo().get_all.return_value = ([mock_user], 1)

        users, total = self.facade.get_users()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['name'], 'Test User')
        self.assertEqual(total, 1)

    @patch('app.persistence.place_repository.PlaceRepository')
    def test_create_place(self, mock_place_repo):
        """
        Teste la méthode create_place de la façade.
        Vérifie que les lieux sont correctement créés.
        """
        place_data = {'title': 'Test Place', 'description': 'A test place', 'owner_id': 'test_owner_id'}  # Ajouter owner_id
        mock_place = Mock(spec=Place)
        mock_place.to_dict.return_value = {'id': '1', **place_data}
        mock_place_repo().add.return_value = mock_place

        result = self.facade.create_place(place_data)

        self.assertEqual(result['title'], 'Test Place')
        self.assertEqual(result['description'], 'A test place')
        self.assertEqual(result['owner_id'], 'test_owner_id')  # Vérifier owner_id

    @patch('app.persistence.review_repository.ReviewRepository')
    @patch('app.persistence.place_repository.PlaceRepository')
    @patch('app.persistence.user_repository.UserRepository')
    def test_create_review(self, mock_user_repo, mock_place_repo, mock_review_repo):
        """
        Teste la méthode create_review de la façade.
        Vérifie que les avis sont correctement créés.
        """
        review_data = {'text': 'Great place!', 'rating': 5, 'user_id': '1', 'place_id': '1'}

        # Simuler la récupération du lieu
        mock_place = Mock(spec=Place)
        mock_place.to_dict.return_value = {'id': '1', 'title': 'Test Place'}
        mock_place_repo().get.return_value = mock_place

        # Simuler la récupération de l'utilisateur
        mock_user = Mock(spec=User)
        mock_user.to_dict.return_value = {'id': '1', 'name': 'Test User'}
        mock_user_repo().get.return_value = mock_user

        # Simuler l'ajout d'une revue
        mock_review = Mock(spec=Review)
        mock_review.to_dict.return_value = {'id': '1', **review_data}
        mock_review_repo().add.return_value = mock_review

        result = self.facade.create_review(review_data)

        self.assertEqual(result['text'], 'Great place!')
        self.assertEqual(result['rating'], 5)

    @patch('app.persistence.amenity_repository.AmenityRepository')
    def test_get_all_amenities(self, mock_amenity_repo):
        """
        Teste la méthode get_all_amenities de la façade.
        Vérifie que les commodités sont correctement récupérées.
        """
        mock_amenity = Mock(spec=Amenity)
        mock_amenity.to_dict.return_value = {'id': '1', 'name': 'WiFi'}
        
        # Retourner une liste de commodités et un total
        mock_amenity_repo().get_all.return_value = ([mock_amenity], 1)

        amenities, total = self.facade.get_all_amenities()

        self.assertEqual(len(amenities), 1)
        self.assertEqual(amenities[0]['name'], 'WiFi')
        self.assertEqual(total, 1)

if __name__ == '__main__':
    unittest.main()
