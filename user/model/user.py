import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from user.enums.gender import GENDER
from utils.phone_number import validate_phone_number
from utils.upload_image import upload_profile_to, validate_image
from .base_user_manager import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    gender_choice = [(gender.value, gender.value) for gender in GENDER]
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number] , unique=True, null=False, blank=False)
    gender = models.CharField(choices=gender_choice,max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to=upload_profile_to, validators=[validate_image], null=False, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    
    class Meta:
        db_table = 'user'
    
    @classmethod
    def is_email_exist(cls, email: str) -> bool:
        """Method to check if te user exists in the database with given email

        Args:
            email (str): Email of the user

        Returns:
            bool: Returns true if the user exists in the database, otherwise false
        """
        return cls.objects.filter(email=email).exists()
    
    @classmethod
    def is_phone_number_exist(cls,phone_number: str) -> bool:
        """Method to check if the phone number of the user already exists in the database

        Args:
            phone_number (str): User phone number

        Returns:
            bool: Returns true if the user phone number already exists in the database, otherwise false
        """
        return cls.objects.filter(phone_number=phone_number).exists()