from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="example@example.com",
            password="verysecurepassword",
            first_name="Test",
            last_name="User"
        )
        self.url = reverse("signin")

    def test_successful_login_sets_jwt_cookie(self):
        response = self.client.post(
            self.url,
            {"email": "example@example.com", "password": "verysecurepassword"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)


    def test_login_with_invalid_password(self):
        response = self.client.post(
            self.url,
            {"email": "example@example.com", "password": "wrong"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Invalid credentials", response.data["detail"])

    def test_login_with_nonexistent_user(self):
        response = self.client.post(
            self.url,
            {"email": "idontexist@example.com", "password": "whatever"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_missing_fields(self):
        response = self.client.post(self.url, {}, format="json")
        print(response.cookies)
        self.assertNotIn('access_token', response.cookies)
        self.assertNotIn('refresh_token', response.cookies)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


