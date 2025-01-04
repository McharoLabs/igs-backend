from decimal import Decimal, InvalidOperation
import uuid
from django.db import models
from django.apps import apps

from account.model.account import Account
from house.enums.availability_status import STATUS
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
from django.db.models import Q, Count
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError

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
    status = models.CharField(max_length=255, choices=STATUS.choices(), default=STATUS.default(), null=False, blank=False)
    is_active_account = models.BooleanField(default=True)
    locked = models.BooleanField(default=False)
    is_full_house_rental = models.BooleanField(default=False, help_text="True if the house is rented as a whole, False if rented by rooms")
    listing_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'house'
        
    def __str__(self) -> str:
        return self.title
    
    def mark_booked(self) -> None:
        """Update the status of the house to 'booked'."""
        self.status = STATUS.BOOKED.value
        self.save()
        
    @classmethod
    def count_total_houses(cls, agent: Agent = None, landlord: LandLord = None) -> int:
        """Counts the total number of houses for the given agent or landlord."""
        if agent and landlord:
            raise ValueError("can not provide both agent and landlord")
        if agent:
            return cls.objects.filter(agent=agent, locked=False, status__in=[STATUS.AVAILABLE.value, STATUS.BOOKED.value]).count()
        elif landlord:
            return cls.objects.filter(landlord=landlord, locked=False, status__in=[STATUS.AVAILABLE.value, STATUS.BOOKED.value]).count()
        else:
            raise ValueError("Either agent or landlord must be provided.")
    
    @classmethod
    def activate_inactive_houses(cls, agent: Agent = None, landlord: LandLord = None):
        """
        Activates all inactive houses associated with the given agent or landlord.

        Args:
            agent (Agent, optional): The agent associated with the houses to activate.
            landlord (LandLord, optional): The landlord associated with the houses to activate.

        Raises:
            ValueError: If both agent and landlord are provided.
        """
        inactive_houses = None
        if agent and landlord:
            raise ValueError("can not provider both agent and landlord")
        if agent:
            inactive_houses = cls.objects.filter(is_active_account=False, locked=False, status=STATUS.AVAILABLE.value, agent=agent)
        if landlord:
            inactive_houses = cls.objects.filter(is_active_account=False, locked=False, status=STATUS.AVAILABLE.value, landlord=landlord)
        
        for house in inactive_houses:
            house.is_active_account = True
            house.save(update_fields=["is_active_account"])
            
    @classmethod
    def deactivate_active_houses(cls, agent: Agent = None, landlord: LandLord = None):
        """
        Deactivates all inactive houses associated with the given agent or landlord.

        Args:
            agent (Agent, optional): The agent associated with the houses to activate.
            landlord (LandLord, optional): The landlord associated with the houses to activate.

        Raises:
            ValueError: If both agent and landlord are provided.
        """
        inactive_houses = None
        if agent and landlord:
            raise ValueError("can not provider both agent and landlord")
        if agent:
            inactive_houses = cls.objects.filter(is_active_account=True, locked=False, status=STATUS.AVAILABLE.value, agent=agent)
        if landlord:
            inactive_houses = cls.objects.filter(is_active_account=True, locked=False, status=STATUS.AVAILABLE.value, landlord=landlord)
        
        for house in inactive_houses:
            house.is_active_account = False
            house.save(update_fields=["is_active_account"])
        
    
    @classmethod
    def mark_sold(cls, house_id: uuid.UUID) -> None:
        house = cls.objects.filter(house_id=house_id).first()
        
        if house is None:
            raise ValidationError("House not found")
        
        house.status = STATUS.SOLD.value
        house.save()
    
    @classmethod
    def get_booked_house(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[House]':
        """Booked house property according to the agent or landlord

        Args:
            agent (Agent, optional): Agent instance to filter houses. Defaults to None.
            landlord (LandLord, optional): Landlord to filter houses. Defaults to None.

        Raises:
            ValidationError: You can not path both agent and landlord, only one required

        Returns:
            QuerySet[House]: A list of house instances if found, otherwise None
        """
        if agent and landlord:
            raise ValidationError("You cannot provide both an agent and a landlord.")
        if agent:
            return cls.objects.filter(status=STATUS.BOOKED.value, agent=agent)
        if landlord:
            return cls.objects.filter(status=STATUS.BOOKED.value, landlord=landlord)
    
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
        filters &= Q(status=STATUS.AVAILABLE.value)
        filters &= Q(is_active_account=True)
        filters &= Q(locked=False)

        if category:
            filters &= Q(category=category)
            if category == CATEGORY.RENTAL.value:
                filters &= Q(is_full_house_rental=True) 
            elif category == CATEGORY.SALE.value:
                filters &= Q(is_full_house_rental=False)
        
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
        return cls.objects.filter(house_id=house_id, status=STATUS.AVAILABLE.value).first()
    
    @classmethod
    def get_all_houses(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[House]':
        """
        This method gets all houses with images uploaded, optionally filtered by agent or landlord,
        ensuring that duplicate houses (due to multiple images) are not returned.

        Returns:
            QuerySet[House]: A list of unique house instances that meet the criteria.

        Raises:
            PermissionDenied: If neither agent nor landlord is provided.
        """
        filters = Q()

        if agent:
            filters &= Q(agent=agent)
        elif landlord:
            filters &= Q(landlord=landlord)
        else:
            raise PermissionDenied("You are not authorized to access the houses without specifying an agent or landlord.")

        houses_with_images = cls.objects.filter(filters).annotate(image_count=Count('house_image')).filter(image_count__gt=0)

        return houses_with_images
        
    @classmethod
    def get_houses_with_no_rooms(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[House]':
        """
        Returns houses that are not full house rentals (is_full_house_rental=False)
        and have no rooms uploaded, optionally filtered by agent or landlord.
        
        Args:
            agent (Agent, optional): The agent requesting the houses. Defaults to None.
            landlord (LandLord, optional): The landlord requesting the houses. Defaults to None.
        
        Raises:
            PermissionDenied: If neither agent nor landlord is specified.
        
        Returns:
            QuerySet[House]: List of houses matching the criteria.
        """
        
        if not (agent or landlord):
            raise PermissionDenied("You are not authorized to access the houses without specifying an agent or landlord.")
        if agent and landlord:
            raise ValueError("Resource can be accessed only by agent or landlord.")
        
        if agent is None and landlord is None:
            raise PermissionDenied("You are not authorized to access the houses without specifying an agent or landlord.")
        
        filters = Q(is_full_house_rental=False)
    
        if agent:
            filters &= Q(agent=agent)
        elif landlord:
            filters &= Q(landlord=landlord)
        
        return cls.objects.filter(filters).annotate(rooms_count=Count('rooms')).filter(rooms_count=0)
    
    @classmethod
    def get_houses_with_no_images(cls, agent: Agent = None, landlord: LandLord = None) -> 'QuerySet[House]':
        """
        Returns houses that do not have any images uploaded, optionally filtered by agent or landlord.

        Args:
            agent (Agent, optional): The agent requesting the houses. Defaults to None.
            landlord (LandLord, optional): The landlord requesting the houses. Defaults to None.

        Raises:
            PermissionDenied: If neither agent nor landlord is specified.

        Returns:
            QuerySet[House]: List of houses matching the criteria.
        """
        
        filters = Q() 

        if not (agent or landlord):
            raise PermissionDenied("You are not authorized to access the houses without specifying an agent or landlord.")
        if agent and landlord:
            raise ValueError("Resource can be accessed only by agent or landlord.")
        
        if agent:
            filters &= Q(agent=agent)
        elif landlord:
            filters &= Q(landlord=landlord)
        
        return cls.objects.filter(filters).annotate(image_count = Count('house_image')).filter(image_count=0)

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
        is_full_house_rental: bool,
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
            is_full_house_rental (bool): Specify if the True the house is full rental, otherwise per room.
            agent (Agent, optional): The agent managing the house. Default is None.
            landlord (LandLord, optional): The landlord of the house. Default is None.

        Returns:
            str: A message indicating successful creation of the house.

        Raises:
            ValueError: If the category is invalid or the price is not a valid decimal.
        """
        
        account = Account.get_account(agent=agent, landlord=landlord)
        
        if account is None:
            raise ValueError("You do not have active account, activate your account to continue")

        total_houses = cls.count_total_houses(agent=agent, landlord=landlord)
        
        if not account.can_upload_house(total_house=cls.count_total_houses(agent=agent, landlord=landlord)):
            raise ValueError("You have reached your maximum house upload limit.")
        
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
            total_bath_room=total_bath_room,
            is_full_house_rental=is_full_house_rental
        )

        house.save()
        logger.info(f'House saved successfully: {house}')
        return f"House '{house.title}' added successfully"
