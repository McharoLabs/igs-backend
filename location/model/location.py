from django.db import models
import uuid

from location.enums.location_type import LOCATION_TYPE

class Location(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    region = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    ward = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_type = models.CharField(max_length=20, choices=[(type.value, type.value) for type in LOCATION_TYPE])

    class Meta:
        db_table = 'location'

    def __str__(self) -> str:
        return f'{self.district} {self.ward}, {self.region}'