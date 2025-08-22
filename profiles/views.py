from rest_framework import generics, permissions
from accounts.models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404


class UserProfileView(generics.RetrieveUpdateAPIView, generics.ListAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    
    def get_object(self):
        user = self.request.user
        if user.is_superuser or user.role == "admin":
            pk = self.kwargs.get("pk")
            if pk:
                return get_object_or_404(User, pk=pk)
            return user  
        return user
