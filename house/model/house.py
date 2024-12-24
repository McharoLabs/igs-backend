from decimal import Decimal, InvalidOperation
import uuid
from django.db import models
from django.apps import apps

from house.enums.category import CATEGORY
from house.enums.condition import CONDITION
from house.enums.furnishing_status import FURNISHING_STATUS
from house.enums.heating_cooling_system import HEATING_COOLING_SYSTEM
from house.enums.security_feature import SECURITY_FEATURES
from location.models import Location
from user.models import Agent
from user.models import LandLord
import logging
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)

class House(models.Model):
    house_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name="houses")
    landlord = models.ForeignKey(LandLord, on_delete=models.SET_NULL, null=True, related_name="houses")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="houses")
    category = models.CharField(max_length=100, choices=CATEGORY.choices(), default=CATEGORY.default(), null=False, blank=False)
    price = models.DecimalField(max_digits=32, decimal_places=2, help_text="The price for the wholee house")
    title = models.CharField(max_length=255)
    description = models.TextField()
    condition = models.CharField(max_length=100, choices=CONDITION.choices(), default=CONDITION.default(), null=False, blank=False)
    nearby_facilities = models.TextField()
    utilities = models.TextField()
    security_features = models.CharField(max_length=255, choices=SECURITY_FEATURES.choices(), default=SECURITY_FEATURES.default(), null=False, blank=False)
    heating_cooling_system = models.CharField(max_length=255, choices=HEATING_COOLING_SYSTEM.choices(), default=HEATING_COOLING_SYSTEM.default(), null=False, blank=False)
    furnishing_status = models.CharField(max_length=255, choices=FURNISHING_STATUS.choices(), default=FURNISHING_STATUS.default(), null=False, blank=False)
    total_bed_room = models.IntegerField()
    total_dining_room = models.IntegerField()
    total_bath_room = models.IntegerField()
    is_available = models.BooleanField(default=True)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'house'
        
    def __str__(self) -> str:
        return self.title
    
    def is_owned_by_agent_or_landlord(self, agent=None, landlord=None) -> bool:
        """Check if the house is owned by the provided agent or landlord.

        Args:
            agent (Agent, optional): The agent to check ownership against. Defaults to None.
            landlord (LandLord, optional): The landlord to check ownership against. Defaults to None.

        Returns:
            bool: True if either the agent or the landlord owns the house, False otherwise.
        """
        if agent and self.agent == agent:
            return True
        if landlord and self.landlord == landlord:
            return True
        return False
    
    def update_house_availability(self) -> None:
        """Update the availability status of this house.

        This method toggles the availability status of the house. If the house is currently 
        available, it will be marked as unavailable, and vice versa.

        Returns:
            bool: True if the availability was successfully updated, False otherwise (e.g., house not found).
        """
        self.is_available = not self.is_available
        self.save()
        return True

    @staticmethod
    def is_house_exists(house_id: uuid.UUID) -> bool:
        """Check if a house with the given ID exists in the database.

        This method checks if a house with the provided house_id exists in the database.

        Args:
            house_id (uuid.UUID): The unique identifier of the house to check.

        Returns:
            bool: True if the house exists, False otherwise.
        """
        return House.objects.filter(house_id=house_id).exists()
    
    @classmethod
    def get_house_by_agent_or_landlord(cls, agent=None, landlord=None, house_id=None) -> 'House':
        """Get a house by agent or landlord and house ID (UUID).
        
        Args:
            agent (Agent, optional): The agent who owns the house. Defaults to None.
            landlord (LandLord, optional): The landlord who owns the house. Defaults to None.
            house_id (UUID, optional): The ID of the house to retrieve. Defaults to None.

        Returns:
            House: The house instance if found, otherwise None.
        """
        if not house_id:
            return None
        
        if agent and landlord:
            raise ValueError("A house can only be associated with either an agent or a landlord, not both.")
        
        filters = Q(house_id=house_id)
        
        if agent:
            filters &= Q(agent=agent)
        if landlord:
            filters &= Q(landlord=landlord)
        
        return cls.objects.filter(filters).first()
    
    @classmethod
    def get_houses_for_agent_or_landlord(cls, agent=None, landlord=None) -> 'QuerySet[House]':
        """Retrieve all houses for the given agent or landlord.

        Args:
            agent (Agent, optional): The agent to get houses for. Defaults to None.
            landlord (LandLord, optional): The landlord to get houses for. Defaults to None.

        Returns:
            QuerySet: A queryset of houses associated with the provided agent or landlord.
        """
        if agent:
            return cls.objects.filter(agent=agent)
        if landlord:
            return cls.objects.filter(landlord=landlord)
        return cls.objects.none()
    
    @classmethod
    def filter_houses(
        cls, 
        category: str = None, 
        region: str = None, 
        district: str = None, 
        min_price: Decimal = None, 
        max_price: Decimal = None, 
    ) -> 'QuerySet[House]':
        
        if category and not CATEGORY.valid(category=category):
            raise ValueError(f"Invalid category '{category}'. Valid options are {', '.join([choice[0] for choice in CATEGORY.choices()])}.")
        
        filters = Q()
        filters &= Q(is_available=True)

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
        
        return cls.objects.filter(filters).select_related('location').order_by('-listing_date')
    
    @classmethod
    def get_house_by_id(cls, house_id: uuid.UUID) -> 'House':
        """This method gets house from the database by using house id

        Args:
            house_id (uuid.UUID): House id to find with

        Returns:
            House: House instance from the database if found, otehrwise None
        """
        return cls.objects.filter(house_id=house_id, is_available=True).first()
    
    @classmethod
    def get_all_houses(cls, agent: Agent = None, landlord: LandLord = None, house_id: uuid.UUID = None) -> 'QuerySet[House]':
        """
        This method gets all the houses, optionally filtered by agent or landlord.

        Returns:
            QuerySet[House]: A list of house instances

        Raises:
            PermissionDenied: If neither agent nor landlord is provided.
        """
        filters = Q()
        
        if house_id:
            filters &= Q(house_id=house_id)
        if agent:
            filters &= Q(agent=agent)
            return cls.objects.filter(filters)
        elif landlord:
            filters &= Q(landlord=landlord)
            return cls.objects.filter(filters)
        else:
            raise PermissionDenied("You are not authorized to access the houses without specifying an agent or landlord.")

    @classmethod
    def add_house(
        cls,
        location: Location,
        title: str,
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
        agent: Agent = None,
        landlord: LandLord = None
    ) -> str:
        """
        Create and save a new House instance to the database.

        Args:
            location (Location): The house's geographical location.
            title (str): The title or name of the house.
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
            agent (Agent, optional): The agent managing the house. Default is None.
            landlord (LandLord, optional): The landlord of the house. Default is None.

        Returns:
            str: A message indicating successful creation of the house.

        Raises:
            ValueError: If the category is invalid or the price is not a valid decimal.
        """
        
        if not CATEGORY.valid(category=category):
            raise ValueError(f"Invalid category '{category}'. Valid options are {', '.join([choice[0] for choice in CATEGORY.choices()])}.")

        try:
            price_value = Decimal(price)
        except InvalidOperation:
            raise ValueError(f"Invalid price '{price}'. It must be a valid decimal number.")

        house = cls(
            agent=agent,
            landlord=landlord,
            location=location,
            category=category,
            title=title,
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
            total_bath_room=total_bath_room
        )

        house.save()
        logger.info(f'House saved successfully: {house}')
        return f"House '{house.title}' added successfully"
