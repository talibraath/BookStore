from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    choices = (('customer', 'Customer'),('admin', 'Admin'),)

    role = models.CharField(max_length=10, choices=choices, default='customer')
