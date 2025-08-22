from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.models import User
from .serializers import UserSerializer, PasswordUpdateSerializer
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


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        new_password = request.data.get("new_password")
        if not new_password:
            return Response({"detail": "New password not provided."},status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"detail": "Password updated successfully."},
                        status=status.HTTP_200_OK)