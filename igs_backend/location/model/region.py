from django.db import models
import uuid
from django.db.models.query import QuerySet
import logging

logger = logging.getLogger(__name__)

class Region(models.Model):
    region_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'region'
        app_label = 'location'
        
    @classmethod
    def is_region_by_name_exists(cls, region_name: str) -> bool:
        """Method to check if the region exists in the database

        Args:
            region_name (str): Region name to be checked

        Returns:
            bool: Return true if the region exists, otehrwise false
        """
        return cls.objects.filter(name=region_name).exists()
    
    @classmethod
    def is_region_by_id_exists(cls, region_id: uuid.UUID) -> bool:
        """Method to check if the region exists in the database

        Args:
            region_id (uuid.UUID): Region id to be checked

        Returns:
            bool: Return true if the region exists, otehrwise false
        """
        return cls.objects.filter(region_id=region_id).exists()
    
    @classmethod
    def get_region_by_id(cls, region_id: uuid.UUID) -> 'Region':
        """Method to get the region by region id from the database

        Args:
            region_id (uuid.UUID): Region id used to get the region from the database

        Returns:
            Region: Region instance from the database if found, otherwise None
        """
        return cls.objects.filter(region_id=region_id).first()

    @staticmethod
    def get_regions() -> 'QuerySet[Region]':
        """Method to get all regions from the database

        Returns:
            QuerySet[Region]: A list of region instances from the database
        """
        return Region.objects.filter()
    
    @classmethod
    def add_region(cls, region_name: str) -> str:
        """This method creates new region and save to the database

        Args:
            region_name (str): Region name to be saved to the database

        Returns:
            str: Message when the region is successful saved
        """
        district = cls(
            name=region_name,
        )
          
        district.save()
        logger.info(f'Region saved successful to the database: {district}')
        return f"Region {district} added successful"