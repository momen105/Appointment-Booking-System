# users/models.py
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from core.models import BaseModel
from .manager import *

class UserModel(AbstractBaseUser,BaseModel):
    USER_TYPE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Patient', 'Patient')
    ]
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    mobile_number = models.CharField(max_length=14)
    division = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    thana = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    license_no = models.CharField(max_length=50, blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'user_type']


    def __str__(self):
        return self.email
    
    class Meta:
        ordering = ["-id"]