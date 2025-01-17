from decimal import Decimal
import uuid
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

from property.models import Property
from user.models import Agent
from house.enums.availability_status import STATUS

import logging

logger = logging.getLogger(__name__)

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.RESTRICT, related_name="bookings", null=False)
    booking_fee = models.DecimalField(max_digits=32, decimal_places=2, null=False, blank=False)
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

        booking = cls.objects.filter(property__status=STATUS.BOOKED.value, property__agent=agent, booking_id=booking_id).first()
        
        if booking:
            if not booking.has_owner_read:
                booking.mark_read()
            return booking

        return None 
    
    @classmethod
    def get_booked_properties(cls, agent: Agent) -> 'QuerySet[Booking]':
        """Retrieve house bookings for an agent  who have booked a house.

        Args:
            agent (Agent, optional): Agent instance to filter houses. Defaults to None.

        Returns:
            QuerySet[Booking]: Filtered queryset of house bookings.
        """
        return cls.objects.filter(property__status=STATUS.BOOKED.value, property__agent=agent)
        
    @classmethod
    def save(cls, property: Property, booking_fee: Decimal) -> str:
        booking = cls(
            property=property,
            booking_fee=booking_fee,
        )

        booking.save()

        return booking
