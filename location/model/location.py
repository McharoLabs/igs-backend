from decimal import Decimal
from django.db import models
import uuid
import logging

logger = logging.getLogger(__name__)

class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    def __str__(self) -> str:
        return f'{self.district} {self.ward}, {self.region}'

    @classmethod
    def add_location(cls, region: str, district: str, ward: str, latitude: Decimal, longitude: Decimal) -> 'Location':
        """This method creates a new location in the database and returns the instance of the newly added location.

        Args:
            region (str): Region name as a string.
            district (str): District name as a string.
            ward (str): Ward name as a string.
            latitude (Decimal): Latitude.
            longitude (Decimal): Longitude.

        Returns:
            Location: The newly created Location instance.
        """
        location = cls(
            region=region,
            district=district,
            ward=ward,
            latitude=latitude,
            longitude=longitude
        )
        location.save()
        logger.info(f"Location saved successfully to the database: {location}")
        return location
