from .views import UserProfileView
from django.urls import path

urlpatterns = [
    path("users/", UserProfileView.as_view()),              
    path("users/<int:pk>/", UserProfileView.as_view()),     
]