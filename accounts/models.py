from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    choices = (('customer', 'Customer'),('admin', 'Admin'),)
    email = models.EmailField(unique=True) 
    role = models.CharField(max_length=10, choices=choices, default='customer')

    otp = models.CharField(max_length=6, blank=True, null=True)
