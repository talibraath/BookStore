from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Register a new user",
        tags=["Auth"], 
        request_body=RegisterSerializer,
        responses={201: openapi.Response(
            description="User registered successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                    'role': openapi.Schema(type=openapi.TYPE_STRING, description='User role'),
                }
            )
        )}
    )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
    @swagger_auto_schema(
        operation_description="Login and obtain JWT tokens",
        tags=["Auth"], 
        request_body=LoginSerializer,
        responses={200: openapi.Response(
            description="Successful login",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'role': openapi.Schema(type=openapi.TYPE_STRING, description='User role'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                }
            )
        )}
    )

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
