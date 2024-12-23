import uuid
from django.db import models
from django.utils import timezone

from house.enums.transaction_type import TRANSACTION_TYPE
from house.model.house import House
from house.model.house_room import Room
from user.model.tenant import Tenant

class HouseTransaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_name="house_transactions")
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room_transactions", null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, related_name="tenant_transactions")
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE.choices(), default=TRANSACTION_TYPE.default(), null=False, blank=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'house_transaction'