import uuid
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet, Q

from property.models import Property
from user.models import Agent
from house.enums.availability_status import STATUS

import logging

from utils.phone_number import validate_phone_number

logger = logging.getLogger(__name__)

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.RESTRICT, related_name="bookings", null=False)
    customer_name = models.CharField(max_length=100, null=False, blank=False)
    customer_email = models.CharField(max_length=100, null=False, blank=False)
    customer_phone_number = models.CharField(max_length=20, null=False, validators=[validate_phone_number], blank=False)
    has_owner_read = models.BooleanField(default=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'booking'
        app_label = 'booking'
        
    def __str__(self) -> str:
        return str(self.booking_id)

    def mark_read(self) -> None:
        """Marks the booking as read by setting has_owner_read to True."""
        if not self.has_owner_read:
            self.has_owner_read = True
            self.save(update_fields=['has_owner_read'])

    @classmethod
    def get_booked_property(cls, booking_id: uuid.UUID, agent: Agent) -> 'Booking':
        """Class method to retrieve booked property for the provided agent

        Args:
            booking_id (uuid.UUID): Booking id to fidn the booking
            agent (Agent): Agent required to retrieve the booking

        Returns:
            Booking | None: Booking instance that matches the given agent and booking ID if found, Otherwise None
        """
        booking: Booking | None = None

        booking = cls.objects.filter(property__status=STATUS.BOOKED.value, property__is_deleted = False, property__agent=agent, booking_id=booking_id).first()
        
        if booking:
            if not booking.has_owner_read:
                booking.mark_read()
            return booking

        return None 
    
    @classmethod
    def get_booked_properties(cls, agent: Agent, customer_name: str = None) -> 'QuerySet[Booking]':
        """Retrieve house bookings for an agent who has booked a house, with optional search by customer name."""
        queryset = cls.objects.filter(property__status=STATUS.BOOKED.value, property__is_deleted = False, property__agent=agent)

        if customer_name:
            queryset = queryset.filter(Q(customer_name__icontains=customer_name))

        return queryset.order_by('-listing_date')
    
    @classmethod
    def save_booking(cls, property: Property, customer_name: str, customer_email: str, customer_phone_number: str) -> None:
        """Save booking details to the database besically after payments completed

        Args:
            property (Property): Property instance booked
            customer_name (str): Customer name for the booking
            customer_email (str): Customer email for the booking
            customer_phone_number (str): Customer phone number for the booking

        Returns:
            Booking: Saved booking instance
        """
        booking = cls(
            property=property,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone_number=customer_phone_number
        )

        booking.save()
