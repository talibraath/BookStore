from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your tests here.
class UserProfileTestCases(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin", 
            password="admin", 
            email="talib@gmail.com",
            role="admin"
        )

        self.customer_user = User.objects.create_user(
            username="test", 
            password="test@1234",
            email="test@gmail.com",
            role="customer"
        )

        self.client = APIClient()

    def authenticate(self, username, password):
        
        data = {
            "username": username,
            "password": password
        }
        response = self.client.post(reverse("login"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        return response
    
    def test_get_user_profile(self):
        self.authenticate("test", "test@1234")
        response = self.client.get("/profile/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_change_user_password(self):
        self.authenticate("test", "test@1234")

        data = {
            "new_password": "newpassword123"
        }
        response = self.client.patch("/profile/users/change-password/",data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_get_other_user_profile(self):
        self.authenticate("admin", "admin")
        response = self.client.get(f"/profile/users/{self.customer_user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)