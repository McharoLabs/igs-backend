import uuid
from django.db import models
from django.db.models.query import QuerySet
from .region import Region
import logging

logger = logging.getLogger(__name__)

class District(models.Model):
    district_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self) -> str:
        return str(self.name)
        
    @classmethod
    def is_district_by_name_exists(cls, district_name: str) -> bool:
        """Method to check if the district already exists in the database

        Args:
            district_name (str): District name

        Returns:
            bool: Returns true if the district exists in the database, otherwise false
        """
        return cls.objects.filter(name=district_name).exists()
    
    @classmethod
    def get_district_by_id(cls, district_id: uuid.UUID) -> 'District':
        """This method gets the district from the database by district id

        Args:
            district_id (uuid.UUID): District id to find the district from the database

        Returns:
            District: District instance from the database if found, otherwise None
        """
        return cls.objects.filter(district_id=district_id).first()
    
    @classmethod
    def get_districts_by_region(cls, region: Region) -> 'QuerySet[District]':
        """This method gets the all districts from the database by region id

        Args:
            region (Region): Region to find the districts from the database

        Returns:
            District: Queryset of District instance from the database if found, otherwise None
        """
        return cls.objects.filter(region=region)

    @classmethod
    def get_district_by_name(cls, district_name: str) -> 'District':
        """Method to get a district by its name

        Args:
            district_name (str): Name of the district

        Returns:
            District: Returns the district object if found, otherwise None
        """
        return cls.objects.filter(name=district_name).first()

    @staticmethod
    def get_all_districts() -> 'QuerySet[District]':
        """Static method to get all districts

        Returns:
            QuerySet: Returns a queryset containing all district objects
        """
        return District.objects.all()
    
    @classmethod
    def add_district(cls, district_name: str, region: Region) -> str:
        """This method creates new district and save to the database

        Args:
            district_name (str): District name to be saved to the database
            region (Region): Instance of the region

        Returns:
            str: Message when the district is successful saved
        """
        district = cls(
            name=district_name,
            region=region
        )
          
        district.save()
        logger.info(f'District saved successful to the database: {district}')
        return f"District {district} added successful"
