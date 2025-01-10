from django.db import models
from property.models import Property


class House(Property):
    total_bed_room = models.IntegerField(null=False)
    total_dining_room = models.IntegerField(null=False)
    total_bath_room = models.IntegerField(null=False)
    
    class Meta:
        db_table = 'house'