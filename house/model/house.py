import uuid
from django.db import models

from location.model.location import Location
from user.model.agent import Agent
from user.model.landlord import Landlord

class House(models.Model):
    house_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name="houses")
    landlord = models.ForeignKey(Landlord, on_delete=models.SET_NULL, null=True, related_name="houses")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="houses")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_unit = models.CharField(max_length=50)
    condition = models.CharField(max_length=100)
    nearby_facilities = models.TextField()
    category = models.CharField(max_length=50)
    utilities = models.TextField()
    security_features = models.TextField()
    heating_cooling_system = models.CharField(max_length=255)
    furnishing_status = models.CharField(max_length=255)
    total_bed_room = models.IntegerField()
    total_dining_room = models.IntegerField()
    total_bath_room = models.IntegerField()
    total_floor = models.IntegerField()

    class Meta:
        db_table = 'house'
        
    def __str__(self) -> str:
        return self.title