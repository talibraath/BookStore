from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BookViewSet, AuthorViewSet, CategoryViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("authors", AuthorViewSet, basename="authors")
router.register("categories", CategoryViewSet, basename="categories")

urlpatterns = [
    
] + router.urls
