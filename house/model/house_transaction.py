from decimal import Decimal
import uuid
from django.db import models
from django.utils import timezone

from house.enums.transaction_type import TRANSACTION_TYPE
from house.model.house import House
from house.model.house_room import Room
from user.model.tenant import Tenant

import logging

logger = logging.getLogger(__name__)

class HouseTransaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_name="house_transactions", null=True)
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room_transactions", null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, related_name="tenant_transactions")
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE.choices(), default=TRANSACTION_TYPE.default(), null=False, blank=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'house_transaction'
        
    @classmethod
    def save_booking(cls, house: House, tenant: Tenant, amount: Decimal, room: Room = None) -> str:
        """
        Save a booking transaction for a tenant in a specific house and room.

        This method creates and saves a booking transaction, which includes details 
        about the house, the tenant, the amount of money paid, and the specific room 
        booked (if any). If no room is specified, it defaults to `None`. After saving 
        the transaction, it logs a success message and returns a confirmation message.

        Args:
            house (House): The house that the tenant is booking.
            tenant (Tenant): The tenant who is making the booking.
            amount (Decimal): The amount paid for the booking.
            room (Room, optional): The specific room booked by the tenant. Defaults to None.

        Returns:
            str: A confirmation message indicating the booking was successfully received.
        """
        transaction = cls(
            house=house,
            room=room,
            tenant=tenant,
            amount=amount,
        )

        transaction.save()

        logger.info(f"Booking saved successfully for: {transaction.tenant}")

        return "Your booking was received successfully"
