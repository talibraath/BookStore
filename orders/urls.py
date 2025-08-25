from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PlaceOrderViewSet

router = DefaultRouter()
router.register(r'', PlaceOrderViewSet, basename='order')
urlpatterns = [

] + router.urls
