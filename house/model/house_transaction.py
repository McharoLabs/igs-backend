from decimal import Decimal
import uuid
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

from house.model.house import House
from house.model.house_room import Room
from user.model.agent import Agent
from user.model.landlord import LandLord
from house.enums.availability_status import STATUS

import logging

logger = logging.getLogger(__name__)

class HouseTransaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_name="house_transactions", null=True)
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room_transactions", null=True)
    booking_fee = models.DecimalField(max_digits=32, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=32, decimal_places=2, null=True)
    is_completed = models.BooleanField(default=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'house_transaction'
        
    def __str__(self) -> str:
        return str(self.transaction_id)
        
    @classmethod
    def get_booked_owner_house(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[HouseTransaction]':
        """Retrieve house transactions for an agent or landlord who have booked a house.

        Args:
            agent (Agent, optional): Agent instance to filter houses. Defaults to None.
            landlord (LandLord, optional): Landlord instance to filter houses. Defaults to None.

        Raises:
            ValidationError: Both agent and landlord cannot be provided.

        Returns:
            QuerySet[HouseTransaction]: Filtered queryset of house transactions.
        """
        if agent and landlord:
            raise ValidationError("You cannot provide both an agent and a landlord, only one required.")
        
        if agent:
            return cls.objects.filter(house__status=STATUS.BOOKED.value, house__agent=agent, is_completed = False)
        
        if landlord:
            return cls.objects.filter(house__status=STATUS.BOOKED.value, house__landlord=landlord, is_completed = False)
        
        return cls.objects.none()
    
    @classmethod
    def get_booked_owner_room(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[HouseTransaction]':
        """Retrieve room transactions for an agent or landlord who have booked a room.

        Args:
            agent (Agent, optional): Agent instance to filter rooms. Defaults to None.
            landlord (LandLord, optional): Landlord instance to filter rooms. Defaults to None.

        Raises:
            ValidationError: Both agent and landlord cannot be provided.

        Returns:
            QuerySet[HouseTransaction]: Filtered queryset of room transactions.
        """
        if agent and landlord:
            raise ValidationError("You cannot provide both an agent and a landlord, only one required.")
        
        if agent:
            return cls.objects.filter(room__status=STATUS.BOOKED.value, room__house__agent=agent, is_completed = False)
        
        if landlord:
            return cls.objects.filter(room__status=STATUS.BOOKED.value, room__house__landlord=landlord, is_completed = False)
        
        return cls.objects.none()
        
    @classmethod
    def save_booking(cls, house: House, booking_fee: Decimal, room: Room = None) -> str:
        """
        Save a booking transaction for a tenant in a specific house and room.

        This method creates and saves a booking transaction, which includes details 
        about the house, the tenant, the amount of money paid, and the specific room 
        booked (if any). If no room is specified, it defaults to `None`. After saving 
        the transaction, it logs a success message and returns a confirmation message.

        Args:
            house (House): The house that the tenant is booking.
            booking_fee (booking_fee): The amount paid for the booking.
            room (Room, optional): The specific room booked by the tenant. Defaults to None.

        Returns:
            str: A confirmation message indicating the booking was successfully received.
        """
        transaction = cls(
            house=house,
            room=room,
            booking_fee=booking_fee,
        )

        transaction.save()

        logger.info(f"Booking saved successfully")

        return "Your booking was received successfully"
