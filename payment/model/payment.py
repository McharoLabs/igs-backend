import uuid
from django.db import models

from house.model.house_transaction import HouseTransaction

class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(HouseTransaction, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'
