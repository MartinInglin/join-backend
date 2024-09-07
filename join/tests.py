from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from join.models import Team

User = get_user_model()


class TeamTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )
        self.team = Team.objects.create(owner=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()

    def test_post_valid_token_valid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {"user_id": 1}
        response = self.client.post("/team/", data=data, format="json")
        self.assertEqual(response.status_code, 200)

    def test_post_valid_token_invalid_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {}
        response = self.client.post("/team/", data=data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_post_no_token(self):
        data = {"user_id": 1}
        response = self.client.post("/team/", data=data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_post_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken123")
        data = {"user_id": 1}
        response = self.client.post("/team/", data=data, format="json")
        self.assertEqual(response.status_code, 401)

        
