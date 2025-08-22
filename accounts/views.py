from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

User = get_user_model()

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
    
        user = User.objects.create_user(  
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            role=validated_data.get("role", "customer"),
            password=validated_data["password"],  
        )
    
        serializer.instance = user  


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        data = {
            'username': user.username,
            'role': user.role,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }   
        return Response(data, status=status.HTTP_200_OK)
