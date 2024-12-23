from decimal import Decimal, InvalidOperation
import uuid
from django.db import models
from django.apps import apps

from house.enums.category import CATEGORY
from house.enums.furnishing_status import FURNISHING_STATUS
from house.enums.heating_cooling_system import HEATING_COOLING_SYSTEM
from house.enums.security_feature import SECURITY_FEATURES
from house.enums.room_category import ROOM_CATEGORY
from location.models import Location
from user.models import Agent
from user.models import LandLord
import logging
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger(__name__)

class House(models.Model):
    house_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name="houses")
    landlord = models.ForeignKey(LandLord, on_delete=models.SET_NULL, null=True, related_name="houses")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="houses")
    category = models.CharField(max_length=100, choices=CATEGORY.choices(), default=CATEGORY.default(), null=False, blank=False)
    price = models.DecimalField(max_digits=32, decimal_places=2, help_text="The price for the whoole house")
    title = models.CharField(max_length=255)
    description = models.TextField()
    condition = models.CharField(max_length=100)
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
    
    @classmethod
    def filter_houses(
        cls, 
        category: str = None, 
        region: str = None, 
        district: str = None, 
        min_price: Decimal = None, 
        max_price: Decimal = None, 
        room_category: str = None, 
        for_whole_house: bool = False
    ) -> 'QuerySet[House]':
        
        if category not in CATEGORY.choices():
            raise ValueError(f"Invalid category '{category}'. Valid options are {CATEGORY.choices()}.")
        
        if room_category not in ROOM_CATEGORY.choices():
            raise ValueError(f"Invalid room category '{room_category}'. Value options are {ROOM_CATEGORY.choices()}")
        
        filters = Q()

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
            
        if category == CATEGORY.SALE.value:
            if min_price:
                filters &= Q(price__gte=min_price)
            if max_price:
                filters &= Q(price__lte=max_price)
        else:
            if for_whole_house:
                if min_price:
                    filters &= Q(price__gte=min_price)
                if max_price:
                    filters &= Q(price__lte=max_price)
                
            else:
                room_filters = Q()
                if room_category:
                    room_filters &= Q(room_category=room_category)
                if min_price:
                    room_filters &= Q(price__gte=min_price)
                if max_price:
                    room_filters &= Q(price__lte=max_price)
                    
                Room = apps.get_model("house", "Room")
                rooms = Room.objects.filter(room_filters)

                filters &= Q(house_id__in=rooms.values('house_id'))
        
        return cls.objects.filter(filters).select_related('location').distinct('house_id').order_by('-listing_date')
    
    @classmethod
    def get_house_by_id(cls, house_id: uuid.UUID) -> 'House':
        """This method gets house from the database by using house id

        Args:
            house_id (uuid.UUID): House id to find with

        Returns:
            House: House instance from the database if found, otehrwise None
        """
        return cls.objects.filter(house_id=house_id).first()
    
    @staticmethod
    def get_all_houses() -> 'QuerySet[House]':
        """This Method gets all the houses from the database

        Returns:
            QuerySet[House]: A list of house instance
        """
        return House.objects.filter()
    
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
        
        if category not in CATEGORY.choices():
            raise ValueError(f"Invalid category '{category}'. Valid options are {CATEGORY.choices()}.")

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
