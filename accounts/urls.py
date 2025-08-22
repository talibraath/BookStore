from django.urls import path
from .views import RegisterView, LoginView, LogoutView
from .views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password-reset-request/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    
    ]
