from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order
from .serializers import OrderSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.pagination  import PageNumberPagination
# Create your views here.

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        return False
       

class PlaceOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    allowd_methods = ['get', 'post','update', 'partial_update']

    def get_queryset(self):
        user = self.request.user

        if user.is_anonymous:
            return Order.objects.none()
        
        if user.role == 'admin':
            return Order.objects.all()
        
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        order = serializer.save()

        items_details = "\n".join([
            f"- {item.book.title} x {item.quantity} @ ${item.price}"
            for item in order.items.all()
        ])

        subject = f"Order Confirmation - Order #{order.id}"
        message = f"""
    Hello {self.request.user.username},

    Thank you for your order! Your order #{order.id} has been successfully placed on {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}.

    Order Details:
    {items_details}

    Total Amount: ${order.total_amount}

    We will notify you once your order is shipped.

    Best regards,
    Your Bookstore Team
    """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.request.user.email, 'f219070@cfd.nu.edu.pk'],
            fail_silently=False
        )

    @action(detail=True, methods=['patch'], url_path='status',permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save(update_fields=['status'])
        send_mail(
            subject=f"Order #{order.id} Status Updated",
            message=f"Hello {order.user.username},\n\nYour order #{order.id} status has been updated to '{new_status}'.\n\nBest regards,\nYour Bookstore Team",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.user.email],
            fail_silently=False,
        )
        return Response({"Status updated successfully."})

    @action(detail=False, methods=['get'], url_path='my-orders', permission_classes=[IsAuthenticated])
    def my_orders(self, request):
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='all-orders', permission_classes=[IsAdmin])
    def all_orders(self, request):
        orders = Order.objects.all()
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)