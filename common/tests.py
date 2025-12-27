from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class APITestBase:
    def create_user(self, email="user@test.com", password="password123"):
        return User.objects.create_user(
            email=email,
            password=password,
            first_name="Test",
            last_name="User"
        )

    def authenticate(self, user):
        client = APIClient()
        response = client.post(
            "/api/v1/auth/login/",
            {"email": user.email, "password": "password123"},
            format="json",
        )
        token = response.data["access"]
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return client
