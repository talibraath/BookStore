from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationTestCase(APITestCase):

    def test_user_registration(self):
        url = reverse("register")  
        data = {
            "username": "testuser",
            "email": "talibraath.nu@gmail.com",
            "password": "test@1234",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(User.objects.filter(username="testuser").exists())

        self.assertIn("id", response.data)
        self.assertEqual(response.data["username"], "testuser")


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="talib.raath",
            email="talib.raath@gmail.com",
            password="test@1234"
        )
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_user_login(self):
        data = {
            "username": "talib.raath",
            "password": "test@1234",
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("username", response.data)
        self.assertIn("access", response.data)
        self.assertIn("role", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["username"], "talib.raath")

   
        refresh_token = response.data["refresh"]
        access_token = response.data["access"]

        data = {
            "refresh": refresh_token
        }

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        logout_response = self.client.post(self.logout_url, data, format="json")

        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertEqual(logout_response.data, "Logout Successfully")

    def test_user_wrong_password(self):
        data = {
            "username": "talib.raath",
            "password": "incorrectpassword",
        }
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)


class PasswordResetTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="talib.raath",
            email="talib.raath@gmail.com",
            password="test@1234"
        )

        self.reset_url = reverse("password-reset")
        self.confirm_url = reverse("password-reset-confirm")
    
    def test_password_reset_request(self):
        url = self.reset_url
        data = {
            "email": "talib.raath@gmail.com"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "OTP sent to your email")

        self.user.otp = "123456"
        self.user.save()
        url = self.confirm_url
        data = {
            "email": "talib.raath@gmail.com",
            "otp": "123456",
            "new_password": "test@1234566"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data['message'], "Password reset successfully")

    
