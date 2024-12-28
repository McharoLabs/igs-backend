from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .user import User
import logging

logger = logging.getLogger(__name__)

class Agent(User):
    pass
    class meta:
        db_table = 'agent'
        
    def __str__(self) -> str:
        return f"{self.first_name} {self.middle_name} {self.last_name}"
        
    @classmethod
    def get_agent_by_phone_number(cls, phone_number: str) -> 'Agent':
        """Retrieve the agent from the database by the phone number

        Args:
            phone_number (str): Phone number to find with

        Returns:
            Agent: Agent instance if found, otherwise None
        """
        return cls.objects.filter(phone_number=phone_number).first()
        
    @classmethod
    def save_agent(cls, first_name: str, middle_name: str, last_name: str, phone_number: str, gender: str, email: str, password: str, avatar=None) -> None:

        if cls.is_email_exist(email=email):
            raise ValidationError(f"An agent with the email '{email}' already exists.")
        if cls.is_phone_number_exist(phone_number=phone_number):
            raise ValidationError(f"An agent with phone number '{phone_number}' already exists.")
        
        try:  
          agent = cls(
              first_name=first_name,
              middle_name=middle_name,
              last_name=last_name,
              phone_number=phone_number,
              gender=gender,
              email=email,
              password=password,
              avatar=avatar if avatar else 'avatars/avatar1.png'
          )
          
          agent.set_password(password)
          agent.save()
          logger.info(f'Agent saved successful to the database: {agent}')
        except IntegrityError as e:
            logger.error(f"There was an issue saving the agent to the database: {e}", exc_info=True)
            raise IntegrityError("There was an issue saving the agent to the database: " + str(e))
        except Exception as e:
            logger.error(f"An unexpected error occurred while saving the agent: {e}", exc_info=True)
            raise Exception(f"An unexpected error occurred while saving the agent: {str(e)}")