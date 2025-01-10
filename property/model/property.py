import uuid
from django.db import models
from django.utils import timezone

from house.enums.availability_status import STATUS
from house.enums.category import CATEGORY
from house.enums.condition import CONDITION
from house.enums.furnishing_status import FURNISHING_STATUS
from house.enums.heating_cooling_system import HEATING_COOLING_SYSTEM
from house.enums.security_feature import SECURITY_FEATURES
from location.models import Location
from user.models import Agent


class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.RESTRICT, null=True, related_name="properties")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="properties")
    category = models.CharField(max_length=100, choices=CATEGORY.choices(), default=CATEGORY.default(), null=False, blank=False)
    price = models.DecimalField(max_digits=32, decimal_places=2)
    description = models.TextField()
    condition = models.CharField(max_length=100, choices=CONDITION.choices(), default=CONDITION.default(), null=False, blank=False)
    nearby_facilities = models.TextField()
    utilities = models.TextField()
    security_features = models.CharField(max_length=255, choices=SECURITY_FEATURES.choices(), default=SECURITY_FEATURES.default(), null=False, blank=False)
    heating_cooling_system = models.CharField(max_length=255, choices=HEATING_COOLING_SYSTEM.choices(), default=HEATING_COOLING_SYSTEM.default(), null=False, blank=False)
    furnishing_status = models.CharField(max_length=255, choices=FURNISHING_STATUS.choices(), default=FURNISHING_STATUS.default(), null=False, blank=False)
    status = models.CharField(max_length=255, choices=STATUS.choices(), default=STATUS.default(), null=False, blank=False)
    is_unread_booking = models.BooleanField(default=False)
    is_active_account = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'property'

    def __str__(self):
        return f"Property {self.property_id}"
    
    def mark_read(self) -> None:
        """Instance method to mark the booking as read.
        """
        if self.is_unread_booking:
            self.is_unread_booking = True
            self.save(update_fields=['is_unread_booking'])
    
    @classmethod
    def total_properties_for_agent(cls, agent: Agent) -> int:
        """Class method to calculate total properties for the specific agent

        Args:
            agent (Agent): Agent instance required to count the total properties

        Returns:
            int: Total number of properties
        """
        return cls.objects.filter(agent=agent).count()