from decimal import Decimal, InvalidOperation
import uuid
from django.db import models
from django.apps import apps
from django.core.exceptions import PermissionDenied, ValidationError

from account.models import Account
from house.enums.availability_status import STATUS
from house.enums.category import CATEGORY
from location.models import Location
from property.models import Property
from user.models import Agent
import logging
from django.db.models.query import QuerySet
from django.db.models import QuerySet, Q, Count, When, Case, IntegerField, Value, OuterRef, Exists


logger = logging.getLogger(__name__)

class House(Property):
    total_bed_room = models.IntegerField(null=False)
    total_dining_room = models.IntegerField(null=False)
    total_bath_room = models.IntegerField(null=False)

    class Meta:
        db_table = 'house'
        app_label = 'house'
        
    def delete(self) -> None:
        self.is_deleted = True
        self.save(update_fields=["is_deleted"], skip_validation=True)
    
    def mark_booked(self) -> None:
        """Update the status of the house to 'booked'."""
        self.status = STATUS.BOOKED.value
        self.save(update_fields=["status"])
        
    @classmethod
    def save_house(
        cls,
        location: Location,
        description: str,
        price: Decimal,
        condition: str,
        nearby_facilities: str,
        category: str,
        utilities: str,
        security_features: str,
        heating_cooling_system: str,
        furnishing_status: str,
        total_bed_room: int,
        total_dining_room: int,
        total_bath_room: int,
        agent: Agent,
        rental_duration: str = None,
    ) -> 'House':
        """
        Create and save a new House instance to the database.

        Args:
            location (Location): The house's geographical location.
            description (str): A detailed description of the house.
            price (Decimal): The price of the house.
            condition (str): The current condition of the house.
            nearby_facilities (str): Facilities close to the house.
            category (str): The category of the house (e.g., residential, commercial).
            utilities (str): Available utilities in the house.
            security_features (str): Security features provided in the house.
            heating_cooling_system (str): Heating or cooling system type.
            furnishing_status (str): Furnishing condition of the house.
            total_bed_room (int): Number of bedrooms.
            total_dining_room (int): Number of dining rooms.
            total_bath_room (int): Number of bathrooms.
            rental_duration (str): Rental duration
            agent (Agent): The agent managing the house.

        Returns:
            House: Saved house instance

        Raises:
            ValueError: If the category is invalid or the price is not a valid decimal.
        """
        
        account = Account.get_account(agent=agent)
        
        if account is None:
            raise PermissionDenied("You do not have active account, activate your account to continue")

        total_properties = cls.total_properties_for_agent(agent=agent)
        
        if not account.can_upload(total_property=total_properties):
            raise PermissionDenied("You have reached your maximum house upload limit.")
        
        if not CATEGORY.valid(category=category):
            raise ValueError(f"Invalid category '{category}'. Valid options are {', '.join([choice[0] for choice in CATEGORY.choices()])}.")

        try:
            price_value = Decimal(price)
        except InvalidOperation:
            raise ValueError(f"Invalid price '{price}'. It must be a valid decimal number.")

        house = cls(
            agent=agent,
            location=location,
            category=category,
            description=description,
            price=price_value,
            condition=condition,
            nearby_facilities=nearby_facilities,
            utilities=utilities,
            security_features=security_features,
            heating_cooling_system=heating_cooling_system,
            furnishing_status=furnishing_status,
            total_bed_room=total_bed_room,
            total_dining_room=total_dining_room,
            total_bath_room=total_bath_room,
            rental_duration=rental_duration,
        )

        house.save()
        return house
    
    @classmethod
    def get_house_by_id(cls, property_id: uuid.UUID ) -> 'House | None':
        """Class method to retrieve house property by given property ID

        Args:
            property_id (uuid.UUID): Unique property ID to retrieve the house property

        Returns:
            House | None: House instance if found, Otherwise None
        """
        return cls.objects.filter(property_id=property_id, is_deleted = False).first()
    
    @classmethod
    def get_agent_house(cls, agent: Agent, property_id: uuid.UUID) -> 'House':
        """Get a house by agent and house ID (UUID).
        
        Args:
            agent (Agent, optional): The agent who owns the house. Defaults to None.
            house_id (UUID, optional): The ID of the house to retrieve. Defaults to None.

        Returns:
            House: The house instance if found, otherwise None.
        """
        
        return cls.objects.filter(property_id=property_id, agent=agent, is_deleted = False).first()
    
    @classmethod
    def get_agent_houses(cls, agent: Agent) -> 'QuerySet[House]':
        """Class method to retrieve agent house properties

        Args:
            agent (Agent): Agent instance

        Returns:
            QuerySet[House]: QuerySet of house instance
        """
        return cls.objects.filter(agent=agent, is_deleted = False).order_by('-listing_date')
    
    @classmethod
    def soft_delete_house(cls, property_id: uuid.UUID, agent: Agent) -> None:
        house = cls.objects.filter(property_id=property_id, agent=agent).first()
        
        if house is None:
            raise ValidationError(message="Mali haipo kwenye mfumo wetu")
        
        house.delete()
    
    @classmethod
    def house_filter(
        cls, 
        category: str = None, 
        region: str = None, 
        district: str = None, 
        min_price: Decimal = None, 
        max_price: Decimal = None,
        ward: str = None, 
        street: str = None
    ) -> 'QuerySet[House]':
        
        if category and not CATEGORY.valid(category=category):
            raise ValueError(f"Invalid category '{category}'. Valid options are {', '.join([choice[0] for choice in CATEGORY.choices()])}.")
        
        filters = Q(status=STATUS.AVAILABLE.value, is_active_account=True, is_deleted=False)

        if category:
            filters &= Q(category=category)
        
        if region:
            filters &= Q(location__region__iexact=region)
        if district:
            filters &= Q(location__district__iexact=district)
            
        if min_price:
            filters &= Q(price__gte=min_price)
        if max_price:
            filters &= Q(price__lte=max_price)
            
        if ward:
            filters &= Q(location__ward__iexact=ward)

        if street:
            filters &= Q(location__street__iexact=street)
        
        paid_account_exists = Account.objects.filter(
            agent=OuterRef("agent"),
            is_active=True,
            plan__is_free=False
        ).values("pk")

        queryset = cls.objects.filter(filters).annotate(
            is_paid=Case(
                When(Exists(paid_account_exists), then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
            image_count=Count('images', distinct=True) 
        ).filter(image_count__gt=0)

        queryset = queryset.select_related('location').order_by('-is_paid', '-listing_date')

        return queryset

    
