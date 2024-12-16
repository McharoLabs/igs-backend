from django.db import models
import uuid

class Region(models.Model):
    region_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        db_table = 'region'
