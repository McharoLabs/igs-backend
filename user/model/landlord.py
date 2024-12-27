from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .user import User
import logging

logger = logging.getLogger(__name__)

class LandLord(User):
    pass
    class Meta:
        db_table = 'landlord'
        
    def __str__(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
        
    @classmethod
    def get_landlord_by_username(cls, username: str) -> 'LandLord':
        """This method gets landlord by username from the database

        Args:
            username (str): username

        Returns:
            LandLord: LandLord instance from the database if found, otherwise None
        """
        return cls.objects.filter(username=username).first()
        
    @classmethod
    def save_landlord(cls, first_name: str, middle_name: str, last_name: str, phone_number: str, gender: str, username: str, email: str, password: str, avatar=None) -> None:

        if cls.is_email_exist(email=email):
            raise ValidationError(f"Land lord with the email '{email}' already exists.")
        if cls.is_username_exist(username=username):
            raise ValidationError(f"Land lord with the username '{username}' already exists.")
        if cls.is_phone_number_exist(phone_number=phone_number):
            raise ValidationError(f"Land lord with phone number '{phone_number}' already exists.")
        
        try:  
          land_lord = cls(
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
          
          land_lord.set_password(password)
          land_lord.save()
          logger.info(f'Land lord saved successful to the database: {land_lord}')
        except IntegrityError as e:
            logger.error(f"There was an issue saving the Land lord to the database: {e}", exc_info=True)
            raise IntegrityError("There was an issue saving the Land lord to the database: " + str(e))
        except Exception as e:
            logger.error(f"An unexpected error occurred while saving the Land lord: {e}", exc_info=True)
            raise Exception(f"An unexpected error occurred while saving the Land lord: {str(e)}")