from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField( max_length=225 , unique=True)
    phone_number = models.CharField(max_length=11 , unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = ['phone_number']
    REQUIRED_FIELDS = ['email'] #only for createsuperuser