from decimal import Decimal
import uuid
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

from house.enums.transaction_type import TRANSACTION_TYPE
from house.model.house import House
from house.model.house_room import Room
from user.model.agent import Agent
from user.model.landlord import LandLord
from user.model.tenant import Tenant
from house.enums.availability_status import STATUS
from .tenant_room import TenantRoom

import logging

logger = logging.getLogger(__name__)

class HouseTransaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_name="house_transactions", null=True)
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room_transactions", null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, related_name="tenant_transactions")
    booking_fee = models.DecimalField(max_digits=32, decimal_places=2, null=False, blank=False)
    amount = models.DecimalField(max_digits=32, decimal_places=2, null=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE.choices(), default=TRANSACTION_TYPE.default(), null=False, blank=False)
    is_completed = models.BooleanField(default=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'house_transaction'
        
    def __str__(self) -> str:
        return str(self.transaction_id)
        
    def complete_transaction(self, amount: Decimal = None) -> None:
        try:
            if self.room:
                if amount is None:
                    raise ValidationError("Amount is required for booking room")
                TenantRoom.tenant_in(amount=amount, tenant=self.tenant, room=self.room)
            elif self.house and not self.room:
                House.mark_sold(house_id=self.house.house_id)
            
            self.is_completed = True
            self.amount = amount
            self.save()
        except ValidationError as e:
            logger.error(f"Failed to complete transaction for {self.transaction_id}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Unexpected error completing transaction {self.transaction_id}: {e}", exc_info=True)

        
    @classmethod
    def cron_house_complete_transaction(cls) -> None:
        bookings = cls.objects.filter(house__status=STATUS.BOOKED.value, is_completed=False)
        if bookings:
            logger.info(f"Trying to auto complete transactions: {[transaction.transaction_id for transaction in bookings]}")
            for booking in bookings:
                try:
                    booking.complete_transaction()
                except Exception as e:
                    logger.error(f"Failed to complete cron transaction for booking {booking.transaction_id}: {e}", exc_info=True)
                    
    @classmethod
    def cron_room_complete_transaction(cls, amount: Decimal) -> None:
        bookings = cls.objects.filter(room__status=STATUS.BOOKED.value, is_completed=False)
        if bookings:
            logger.info(f"Trying to auto complete transactions: {[transaction.transaction_id for transaction in bookings]}")
            for booking in bookings:
                try:
                    booking.complete_transaction(amount)
                except Exception as e:
                    logger.error(f"Failed to complete cron transaction for booking {booking.transaction_id}: {e}", exc_info=True)

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
    def get_booked_tenant_house(cls, tenant: Tenant) -> 'QuerySet[HouseTransaction]':
        """Retrieve house transactions for a specific tenant who has booked a room.

        Args:
            tenant (Tenant): The tenant instance whose bookings we are fetching.

        Returns:
            QuerySet[HouseTransaction]: Filtered queryset of house transactions.
        """
        if not tenant:
            raise ValidationError("Tenant instance is required.")

        return cls.objects.filter(tenant=tenant, house__status = STATUS.BOOKED.value, is_completed = False)
    
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
    def get_booked_tenant_room(cls, tenant: Tenant = None) -> 'QuerySet[HouseTransaction]':
        """Retrieve room transactions for a specific tenant who has booked a room.

        Args:
            tenant (Tenant): The tenant instance whose bookings we are fetching.

        Returns:
            QuerySet[HouseTransaction]: Filtered queryset of room transactions.
        """
        if tenant is None:
            raise ValidationError("Tenant instance is required.")
        
        return cls.objects.filter(room__status=STATUS.BOOKED.value, tenant=tenant, is_completed = False)
        
    @classmethod
    def save_booking(cls, house: House, tenant: Tenant, booking_fee: Decimal, room: Room = None) -> str:
        """
        Save a booking transaction for a tenant in a specific house and room.

        This method creates and saves a booking transaction, which includes details 
        about the house, the tenant, the amount of money paid, and the specific room 
        booked (if any). If no room is specified, it defaults to `None`. After saving 
        the transaction, it logs a success message and returns a confirmation message.

        Args:
            house (House): The house that the tenant is booking.
            tenant (Tenant): The tenant who is making the booking.
            booking_fee (booking_fee): The amount paid for the booking.
            room (Room, optional): The specific room booked by the tenant. Defaults to None.

        Returns:
            str: A confirmation message indicating the booking was successfully received.
        """
        transaction = cls(
            house=house,
            room=room,
            tenant=tenant,
            booking_fee=booking_fee,
        )

        transaction.save()

        logger.info(f"Booking saved successfully for: {transaction.tenant}")

        return "Your booking was received successfully"
