from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .user import User
import logging

logger = logging.getLogger(__name__)

class Tenant(User):
    pass
    class Meta:
        db_table = 'tenant'
        
    @classmethod
    def save_tenant(cls, first_name: str, middle_name: str, last_name: str, phone_number: str, gender: str, username: str, email: str, password: str, avatar=None) -> None:

        if cls.is_email_exist(email=email):
            raise ValidationError(f"Tenant with the email '{email}' already exists.")
        if cls.is_username_exist(username=username):
            raise ValidationError(f"Tenant with the username '{username}' already exists.")
        if cls.is_phone_number_exist(phone_number=phone_number):
            raise ValidationError(f"Tenant with phone number '{phone_number}' already exists.")
        
        try:  
          tenant = cls(
              first_name=first_name,
              middle_name=middle_name,
              last_name=last_name,
              phone_number=phone_number,
              gender=gender,
              username=username,
              email=email,
              password=password,
              avatar=avatar if avatar else 'avatars/avatar1.png'
          )
          
          tenant.set_password(password)
          tenant.save()
          logger.info(f'Tenant saved successful to the database: {tenant}')
        except IntegrityError as e:
            logger.error(f"There was an issue saving the tenant to the database: {e}", exc_info=True)
            raise IntegrityError("There was an issue saving the tenant to the database: " + str(e))
        except Exception as e:
            logger.error(f"An unexpected error occurred while saving the tenant: {e}", exc_info=True)
            raise Exception(f"An unexpected error occurred while saving the tenant: {str(e)}")