import uuid
from django.db import models

from .region import Region


class District(models.Model):
    district_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=False, blank=False)
    
    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'district'