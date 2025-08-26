from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random
from django.core.mail import send_mail
from .serializers import ResetPasswordSerializer
from django.conf import settings


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


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Logout and blacklist the refresh token",
        tags=["Auth"], 
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
            },
            required=['refresh']
        ),
        responses={
            205: openapi.Response(description="Successful logout"),
            400: openapi.Response(description="Bad request")
        }
    )

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Logout Successfully",status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(
        operation_description="Request password reset OTP",
        tags=["Auth"], 
        request_body=ResetPasswordSerializer,
        responses={200: openapi.Response(
            description="OTP sent to email",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                }
            )
        )}
    )

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))  
            user.otp = otp
            user.save()

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP for password reset is: {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
    

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(
        operation_description="Confirm password reset with OTP",
        tags=["Auth"], 
        request_body=ResetPasswordSerializer,
        responses={200: openapi.Response(
            description="Password reset successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                }
            )
        )}
    )

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        if not email or not otp or not new_password:
            return Response({"error": "Email, OTP, and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, otp=otp)
            user.set_password(new_password)
            user.otp = None  
            user.save()

            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or OTP"}, status=status.HTTP_404_NOT_FOUND)
        
    