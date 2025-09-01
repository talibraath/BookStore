from django.urls import path
from .views import MoodRecommendationView, BookSummaryView

urlpatterns = [
    path("mood-ai/", MoodRecommendationView.as_view(), name="mood-recommendations"),
    path("book-summary/<int:id>/", BookSummaryView.as_view(), name="book-summary"),

]
