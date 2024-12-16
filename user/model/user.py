import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from user.enums.gender import GENDER
from .base_user_manager import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    gender_choice = [(gender.value, gender.value) for gender in GENDER]
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(choices=gender_choice,max_length=50, null=False, blank=False)
    username = models.CharField(verbose_name='username', unique=True, max_length=50)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars', null=False, blank=True, default='avatars/avatar1.png')
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['phone_number', 'email']
    
    class Meta:
        db_table = 'user'