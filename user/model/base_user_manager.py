from django.contrib.auth.models import BaseUserManager
from django.db import transaction

class MyUserManager(BaseUserManager):
    def create_user(self, first_name: str, last_name: str, middle_name:str = None, email: str=None, phone_number: str=None, password: str=None, **extra_fields):
        """
        Creates and saves a regular user with the given  email, phone number, and password.
        """

        if not email:
            raise ValueError("The Email field is required.")
        if not phone_number:
            raise ValueError("The Phone Number field is required.")
        if not password:
            raise ValueError("The password is required")

        email = self.normalize_email(email)

        # Create User instance
        user = self.model(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    @transaction.atomic
    def create_superuser(self, first_name, last_name, middle_name=None, email=None, phone_number=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, phone number, and password.
        """
        # Set superuser-specific flags
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        # Create user and corresponding UserAuth
        return self.create_user(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
