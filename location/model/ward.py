import uuid
from django.db import models
from django.db.models.query import QuerySet

from .district import District
import logging

logger = logging.getLogger(__name__)

class Ward(models.Model):
    ward_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'ward'
        app_label = 'location'
        
    @classmethod
    def is_ward_by_name_exists(cls, ward_name: str) -> bool:
        """Method to check if the ward already exists in the database

        Args:
            ward_name (str): ward name

        Returns:
            bool: Returns true if the ward exists in the database, otherwise false
        """
        return cls.objects.filter(name=ward_name).exists()
    
    @classmethod
    def get_ward_by_id(cls, ward_id: uuid.UUID) -> 'Ward':
        """This method gets the ward from the database by ward id

        Args:
            ward_id (uuid.UUID): ward id to find the ward from the database

        Returns:
            ward: ward instance from the database if found, otherwise None
        """
        return cls.objects.filter(ward_id=ward_id).first()
    
    @classmethod
    def get_wards_by_district(cls, district: District) -> 'QuerySet[Ward]':
        """This method gets the all wards from the database by district id

        Args:
            district (District): District to find the wards from the database

        Returns:
            ward: Queryset of ward instance from the database if found, otherwise None
        """
        return cls.objects.filter(district=district)

    @classmethod
    def get_ward_by_name(cls, ward_name: str) -> 'Ward':
        """Method to get a ward by its name

        Args:
            ward_name (str): Name of the ward

        Returns:
            ward: Returns the ward object if found, otherwise None
        """
        return cls.objects.filter(name=ward_name).first()

    @staticmethod
    def get_all_wards() -> 'QuerySet[Ward]':
        """Static method to get all wards

        Returns:
            QuerySet: Returns a queryset containing all ward objects
        """
        return Ward.objects.all()

