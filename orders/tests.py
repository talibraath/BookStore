from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Book, Order
from catalog.models import Author, Category

User = get_user_model()

class OrderAPITestCase(APITestCase):

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

        self.author = Author.objects.create(name="Talib Raath")
        self.category = Category.objects.create(name="Adventure")

        self.book = Book.objects.create(
            title="Titanic",
            author=self.author,
            category=self.category,
            price=120.0,
            pub_date="2025-08-13",
            stock=10
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
    
    def test_customer_create_order(self):
        url = reverse("order-list")
        self.authenticate("test", "test@1234")

        data = {
            "items": [
                {
                "book": self.book.id,
                "quantity": 2
                }
                ]
            }
        
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.customer_user.id)
        self.assertEqual(float(response.data["total_amount"]), 240.0)
    
    def test_admin_create_order(self):
        url = reverse("order-list")
        self.authenticate("admin", "admin")

        data = {
            "items": [
                {
                "book": self.book.id,
                "quantity": 2
                }
                ]
            }
        
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.admin_user.id)
        self.assertEqual(float(response.data["total_amount"]), 240.0)

    def test_admin_list_order(self):
        url = reverse("order-list")
        self.authenticate("admin", "admin")
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_list_order(self):
        url = reverse("order-list")
        self.authenticate("test", "test@1234")
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_update_order_status(self):
        url = reverse("order-list")
        self.authenticate("admin", "admin")

        data = {
            "items": [
                {
                "book": self.book.id,
                "quantity": 2
                }
                ]
            }
        
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data["total_amount"]), 240.0)

        url = reverse("order-update-status", args=[response.data["id"]]) 
        
        data = {
            "status": "shipped"
            }
        response = self.client.patch(url,data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
