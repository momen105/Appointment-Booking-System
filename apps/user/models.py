# users/models.py
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from core.models import BaseModel
from .manager import *



class Division(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class District(BaseModel):
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.name} ({self.division.name})"

class Thana(BaseModel):
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='thanas')
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.name} ({self.district.name})"

class UserModel(AbstractBaseUser,BaseModel,PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient')
    ]
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    mobile_number = models.CharField(max_length=14)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=True)
    thana = models.ForeignKey(Thana, on_delete=models.CASCADE, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'



    def __str__(self):
        return self.email
    



    class Meta:
        ordering = ["-id"]