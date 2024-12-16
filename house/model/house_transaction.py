import uuid
from django.db import models

from house.enums.transaction_type import TRANSACTION_TYPE

from .house import House

class HouseTransaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=[(type.value, type.value) for type in TRANSACTION_TYPE])
    price = models.DecimalField(max_digits=32, decimal_places=2)
    available_room = models.IntegerField(null=True, blank=True)  # Only for rental
    is_available = models.BooleanField(default=True)  # Only for sale

    class Meta:
        db_table = 'house_transaction'