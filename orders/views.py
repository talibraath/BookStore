from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.pagination  import PageNumberPagination
from .signals import order_confirmed
from rest_framework import status
from django.core.cache import cache

# Create your views here.
class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_authenticated and request.method in ['GET', 'POST'] and request.user.role in 'customer':
            return True            
        
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        return False
       

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch']    
    
    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Order.objects.none()
        
        if user.role == 'admin':
            key = "all_orders"
            cached_orders = cache.get(key)

            if cached_orders:
                return cached_orders
            
            all_orders = Order.objects.all().order_by('-created_at')
            cache.set(key, all_orders, 60*5)

            return all_orders
        
        key = f"user_order_{user.id}"
        
        cached_user_orders = cache.get(key)

        if cached_user_orders:

            return cached_user_orders
        
        user_orders =  Order.objects.filter(user=user).order_by('-created_at')
        cache.set(key, user_orders, 60*5)
        return user_orders
    
    def perform_create(self, serializer):
        order = serializer.save()
        user = self.request.user
        cache.delete(f"user_order_{user.id}")
        cache.delete("all_orders")
        order_confirmed.send(sender=Order, order=order, user=user)
 
    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        cache.delete(f"user_order_{order.user.id}")
        cache.delete("all_orders")
        order.save(update_fields=['status'])

        return Response({"Status updated successfully."})
    