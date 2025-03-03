from typing import List
import uuid
from django.db import models
from django.http import Http404
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from account.models import Account
from house.enums.availability_status import STATUS
from house.enums.category import CATEGORY
from house.enums.condition import CONDITION
from house.enums.furnishing_status import FURNISHING_STATUS
from house.enums.heating_cooling_system import HEATING_COOLING_SYSTEM
from property.enums.rental_duration import RENTAL_DURATION
from house.enums.security_feature import SECURITY_FEATURES
from location.models import Location
from user.models import Agent
import logging
from django.db.models import QuerySet, Q, Count, When, Case, IntegerField, Value, OuterRef, Exists


logger = logging.getLogger(__name__)

class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.RESTRICT, null=False, related_name="properties")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="properties")
    category = models.CharField(max_length=100, choices=CATEGORY.choices(), default=CATEGORY.default(), null=False, blank=False)
    price = models.DecimalField(max_digits=32, decimal_places=2)
    rental_duration = models.CharField(max_length=50, choices=RENTAL_DURATION.choices(), default=None, null=True, blank=True)
    description = models.TextField()
    condition = models.CharField(max_length=100, choices=CONDITION.choices(), default=CONDITION.default(), null=False, blank=False)
    nearby_facilities = models.TextField()
    utilities = models.TextField()
    security_features = models.CharField(max_length=255, choices=SECURITY_FEATURES.choices(), default=SECURITY_FEATURES.default(), null=False, blank=False)
    heating_cooling_system = models.CharField(max_length=255, choices=HEATING_COOLING_SYSTEM.choices(), default=HEATING_COOLING_SYSTEM.default(), null=False, blank=False)
    furnishing_status = models.CharField(max_length=255, choices=FURNISHING_STATUS.choices(), default=FURNISHING_STATUS.default(), null=False, blank=False)
    status = models.CharField(max_length=255, choices=STATUS.choices(), default=STATUS.default(), null=False, blank=False)
    is_active_account = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = False
        db_table = 'property'
        app_label = 'property'

    def __str__(self):
        return f"Property {self.property_id}"
    
    def available(self) -> bool:
        return self.status == STATUS.AVAILABLE.value and not self.is_deleted
    
    def mark_booked(self) -> None:
        self.status = STATUS.BOOKED.value
        self.save(update_fields=['status'])
        
    def clean(self):
        """Ensure `rental_duration` is only provided for rental properties."""
        if self.category == CATEGORY.RENTAL.value and not self.rental_duration:
            raise ValidationError({"rental_duration": "Rental properties must have a rental duration."})
        if self.category == CATEGORY.SALE.value and self.rental_duration:
            raise ValidationError({"rental_duration": "Sale properties should not have a rental duration."})

    def save(self, *args, **kwargs):
        """Run model validation before saving."""
        skip_validation = kwargs.pop('skip_validation', False)
        
        if not skip_validation:
            self.full_clean() 
        
        super().save(*args, **kwargs)

        
    @classmethod
    def demo_properties(cls) -> 'QuerySet[Property]':
        """Retrieves demo property and uncategorized property

        Returns:
            QuerySet[Property]: Property instances queryset
        """
        paid_account_exists = Account.objects.filter(
            agent=OuterRef("agent"),
            is_active=True,
            plan__is_free=False
        ).values("pk")

        queryset = cls.objects.filter(is_active_account = True, is_deleted = False).annotate(
            is_paid=Case(
                When(Exists(paid_account_exists), then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
            image_count=Count('images', distinct=True) 
        ).filter(image_count__gt=0) 

        queryset = queryset.select_related('location').order_by('-is_paid', '-listing_date')

        return queryset
        
    @classmethod
    def mark_property_rented(cls, property_id: uuid.UUID, agent: Agent) -> None:
        property = cls.objects.filter(property_id=property_id, status=STATUS.BOOKED.value, agent=agent).first()
        
        if property is None:
            raise Http404("Property not found or not in the booked status.")
        
        property.status = STATUS.RENTED.value
        property.save(update_fields=['status'])
        
    @classmethod
    def mark_property_available(cls, property_id: uuid.UUID, agent: Agent) -> None:
        property = cls.objects.filter(
            is_deleted = False,
            property_id=property_id,
            agent=agent,
            status__in=[STATUS.RENTED.value, STATUS.SOLD.value, STATUS.BOOKED.value]
        ).first()
        
        if property is None:
            raise Http404("Property not found or not in rented or sold or booked status.")
        
        property.status = STATUS.AVAILABLE.value
        property.save(update_fields=['status'])
        
    @classmethod
    def mark_property_sold(cls, property_id: uuid.UUID, agent: Agent) -> None:
        property = cls.objects.filter(property_id=property_id, status=STATUS.SOLD.value, agent=agent).first()
        
        if property is None:
            raise Http404("Property not found or not in the sold status.")
        
        property.status = STATUS.SOLD.value
        property.save(update_fields=['status'])
    
    @classmethod
    def total_properties_for_agent(cls, agent: Agent) -> int:
        """Class method to calculate total properties for the specific agent

        Args:
            agent (Agent): Agent instance required to count the total properties

        Returns:
            int: Total number of properties
        """
        return cls.objects.filter(agent=agent, is_deleted = False).count()
    
    @classmethod
    def get_property_by_id(cls, property_id: uuid.UUID) -> 'Property | None':
        """Class method to retrieve property instance

        Args:
            property_id (uuid.UUID): Unique property id to retrieve the instance

        Returns:
            Property | None: Instance of property that matches the property ID if found, otherwise None
        """
        return cls.objects.filter(property_id=property_id, is_deleted = False).first()
    
    @classmethod
    def get_property_for_booking(cls, property_id: uuid.UUID) -> 'Property | None':
        """Class method to retrieve property instance

        Args:
            property_id (uuid.UUID): Unique property id to retrieve the instance

        Returns:
            Property | None: Instance of property that matches the property ID if found, otherwise None
        """
        return cls.objects.filter(property_id=property_id, status=STATUS.AVAILABLE.value, is_deleted = False).first()
    
    @classmethod
    def get_agent_property_by_id(cls, agent: Agent, property_id: uuid.UUID) -> 'Property | None':
        """Class method to retrieve property for the given agent and property ID

        Args:
            agent (Agent): Agent instance
            property_id (uuid.UUID): Unique property ID

        Returns:
            Property | None: Property instance that matches the criteria provided if found, Otherwise None
        """
        return cls.objects.filter(agent=agent, property_id=property_id, is_deleted = False).first()
    
    @classmethod
    def activate_inactive_properties(cls, agent: Agent):
        """
        Activates all inactive houses associated with the given agent.

        Args:
            agent (Agent, optional): The agent associated with the houses to activate.

        Raises:
            ValueError: If both agent are provided.
        """
        inactive_houses = None
        
        inactive_houses = cls.objects.filter(is_active_account=False, is_deleted=False, agent=agent)
        
        for house in inactive_houses:
            house.is_active_account = True
            house.save(update_fields=["is_active_account"], skip_validation=True)
            
    @classmethod
    def deactivate_active_properties(cls, agent: Agent):
        """
        Deactivates all inactive houses associated with the given agent.

        Args:
            agent (Agent, optional): The agent associated with the houses to activate.
        """
        inactive_houses = None
        
        inactive_houses = cls.objects.filter(is_active_account=True, is_deleted=False, agent=agent)
        
        for house in inactive_houses:
            house.is_active_account = False
            house.save(update_fields=["is_active_account"], skip_validation=True)
