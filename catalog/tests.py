from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Author, Category, Book
from datetime import date

User = get_user_model()

class BookstoreAPITestCase(APITestCase):

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
            pub_date="2025-08-13"
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

    def test_customer_list_authors(self):
        self.authenticate("test", "test@1234")
        url = reverse("authors-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_list_authors(self):
        self.authenticate("admin", "admin")
        url = reverse("authors-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_author(self):
        self.authenticate("admin", "admin")
        url = reverse("authors-list")
        data = {"name": "Husain"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category(self):
        self.authenticate("admin", "admin")
        url = reverse("categories-list")
        data = {"name": "Fantasy"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_category(self):
        self.authenticate("test", "test@1234")
        url = reverse("categories-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_books(self):
        self.authenticate("test", "test@1234")
        url = reverse("books-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_books(self):
        self.authenticate("admin", "admin")
        url = reverse("books-list")
        data = {
            "title": "Testcase Book",
            "author": self.author.id,
            "category": self.category.id,
            "price": 150.0,
            "pub_date": date.today()
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
