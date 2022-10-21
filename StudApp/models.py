from django.db import models
from rest_framework import authentication
from rest_framework.authtoken.models import Token
from .manager import UserManager
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
  
    email = models.EmailField(max_length=200, unique=True)
    #username=models.EmailField(max_length=200, unique=True)
    otp = models.CharField(max_length=200 , null=True, blank=True)   
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.email

class Student(models.Model):
    name = models.CharField(max_length=100, blank= True, null=True)
    mobile = models.CharField(max_length=15, blank= True, null=True)

    def __str__(self):
        return self.name

