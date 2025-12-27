from django.test import TestCase
from rest_framework.test import APIClient


class AuthTests(TestCase):
    def test_user_can_register_and_login(self):
        client = APIClient()

        # Register
        res = client.post(
            "/api/v1/auth/register/",
            {
                "email": "auth@test.com",
                "password": "password123",
                "first_name": "Auth",
                "last_name": "User",
            },
            format="json",
        )
        self.assertEqual(res.status_code, 201)

        # Login
        res = client.post(
            "/api/v1/auth/login/",
            {"email": "auth@test.com", "password": "password123"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
