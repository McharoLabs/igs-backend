from decimal import Decimal
import uuid
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError

from house.models import House
from house.models import Room
from user.models import Agent
from user.models import LandLord
from house.enums.availability_status import STATUS

import logging

logger = logging.getLogger(__name__)

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_name="house_booking", null=False)
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room_booking", null=True)
    booking_fee = models.DecimalField(max_digits=32, decimal_places=2, null=False, blank=False)
    has_owner_read = models.BooleanField(default=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'booking'
        
    def __str__(self) -> str:
        return str(self.booking_id)

    def mark_read(self) -> None:
        """Marks the booking as read by setting has_owner_read to True."""
        if not self.has_owner_read:
            self.has_owner_read = True
            self.save()

    @classmethod
    def get_booked_owner_house(cls, booking_id: uuid.UUID = None, agent: Agent = None, landlord: LandLord = None) -> 'Booking':
        """Retrieve house booking for an agent or landlord who have booked a house.

        Args:
            agent (Agent, optional): Agent instance to filter house. Defaults to None.
            landlord (LandLord, optional): Landlord instance to filter house. Defaults to None.

        Raises:
            ValidationError: Both agent and landlord cannot be provided.

        Returns:
            Booking: House booking instance.
        """
        if not booking_id:
            raise ValidationError("Booking id is required")
        
        if agent and landlord:
            raise ValidationError("You cannot provide both an agent and a landlord, only one required.")
        
        booking = None

        if agent:
            booking = cls.objects.filter(house__status=STATUS.BOOKED.value, house__agent=agent, booking_id=booking_id).first()
        
        if landlord:
            booking = cls.objects.filter(house__status=STATUS.BOOKED.value, house__landlord=landlord, booking_id=booking_id).first()
        
        if booking:
            if not booking.has_owner_read:
                booking.mark_read()
            return booking

        return None 
    
    @classmethod
    def get_booked_owner_room(cls, booking_id: uuid.UUID = None, agent: Agent = None, landlord: LandLord = None) -> 'Booking':
        """Retrieve room bookings for an agent or landlord who have booked a room.

        Args:
            agent (Agent, optional): Agent instance to filter room. Defaults to None.
            landlord (LandLord, optional): Landlord instance to filter room. Defaults to None.

        Raises:
            ValidationError: Both agent and landlord cannot be provided.

        Returns:
            Booking: Room booking instance.
        """
        if booking_id is None:
            raise ValidationError("Booking id is required")
        if agent and landlord:
            raise ValidationError("You cannot provide both an agent and a landlord, only one required.")
        
        booking = None
        
        if agent:
            booking = cls.objects.filter(room__status=STATUS.BOOKED.value, room__house__agent=agent, booking_id=booking_id).first()
        
        if landlord:
            booking = cls.objects.filter(room__status=STATUS.BOOKED.value, room__house__landlord=landlord, booking_id=booking_id).first()
        
        if booking:
            if not booking.has_owner_read:
                booking.mark_read()
            return booking

        return None
    
    @classmethod
    def get_booked_owner_houses(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[Booking]':
        """Retrieve house bookings for an agent or landlord who have booked a house.

        Args:
            agent (Agent, optional): Agent instance to filter houses. Defaults to None.
            landlord (LandLord, optional): Landlord instance to filter houses. Defaults to None.

        Raises:
            ValidationError: Both agent and landlord cannot be provided.

        Returns:
            QuerySet[Booking]: Filtered queryset of house bookings.
        """
        if agent and landlord:
            raise ValidationError("You cannot provide both an agent and a landlord, only one required.")
        
        if agent:
            return cls.objects.filter(house__status=STATUS.BOOKED.value, house__agent=agent)
        
        if landlord:
            return cls.objects.filter(house__status=STATUS.BOOKED.value, house__landlord=landlord)
        
        return cls.objects.none()
    
    @classmethod
    def get_booked_owner_rooms(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[Booking]':
        """Retrieve room bookings for an agent or landlord who have booked a room.

        Args:
            agent (Agent, optional): Agent instance to filter rooms. Defaults to None.
            landlord (LandLord, optional): Landlord instance to filter rooms. Defaults to None.

        Raises:
            ValidationError: Both agent and landlord cannot be provided.

        Returns:
            QuerySet[Booking]: Filtered queryset of room bookings.
        """
        if agent and landlord:
            raise ValidationError("You cannot provide both an agent and a landlord, only one required.")
        
        if agent:
            return cls.objects.filter(room__status=STATUS.BOOKED.value, room__house__agent=agent)
        
        if landlord:
            return cls.objects.filter(room__status=STATUS.BOOKED.value, room__house__landlord=landlord)
        
        return cls.objects.none()
        
    @classmethod
    def save_booking(cls, house: House, booking_fee: Decimal, room: Room = None) -> str:
        """
        Save a booking booking for a tenant in a specific house and room.

        This method creates and saves a booking booking, which includes details 
        about the house, the tenant, the amount of money paid, and the specific room 
        booked (if any). If no room is specified, it defaults to `None`. After saving 
        the booking, it logs a success message and returns a confirmation message.

        Args:
            house (House): The house that the tenant is booking.
            booking_fee (booking_fee): The amount paid for the booking.
            room (Room, optional): The specific room booked by the tenant. Defaults to None.

        Returns:
            str: A confirmation message indicating the booking was successfully received.
        """
        booking = cls(
            house=house,
            room=room,
            booking_fee=booking_fee,
        )

        booking.save()

        logger.info(f"Booking saved successfully")

        return "Your booking was received successfully"
