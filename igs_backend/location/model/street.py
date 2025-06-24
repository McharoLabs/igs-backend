import uuid
from django.db import models
from django.db.models.query import QuerySet

import logging

from .ward import Ward

logger = logging.getLogger(__name__)

class Street(models.Model):
    street_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'street'
        app_label = 'location'
        
    @classmethod
    def is_street_by_name_exists(cls, street_name: str) -> bool:
        """Method to check if the street already exists in the database

        Args:
            street_name (str): street name

        Returns:
            bool: Returns true if the street exists in the database, otherwise false
        """
        return cls.objects.filter(name=street_name).exists()
    
    @classmethod
    def get_street_by_id(cls, street_id: uuid.UUID) -> 'Street':
        """This method gets the street from the database by street id

        Args:
            street_id (uuid.UUID): street id to find the street from the database

        Returns:
            street: street instance from the database if found, otherwise None
        """
        return cls.objects.filter(street_id=street_id).first()
    
    @classmethod
    def get_streets_by_Ward(cls, ward: Ward) -> 'QuerySet[Street]':
        """This method gets the all streets from the database by Ward id

        Args:
            Ward (Ward): Ward to find the streets from the database

        Returns:
            street: Queryset of street instance from the database if found, otherwise None
        """
        return cls.objects.filter(ward=ward)

    @classmethod
    def get_street_by_name(cls, street_name: str) -> 'Street':
        """Method to get a street by its name

        Args:
            street_name (str): Name of the street

        Returns:
            street: Returns the street object if found, otherwise None
        """
        return cls.objects.filter(name=street_name).first()

    @staticmethod
    def get_all_streets() -> 'QuerySet[Street]':
        """Static method to get all streets

        Returns:
            QuerySet: Returns a queryset containing all street objects
        """
        return Street.objects.all()

