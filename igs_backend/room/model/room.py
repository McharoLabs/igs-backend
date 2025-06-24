from decimal import Decimal
import uuid
from django.db import models
from account.models import Account
from house.enums.availability_status import STATUS
from house.enums.category import CATEGORY
from house.enums.room_category import ROOM_CATEGORY
from location.models import Location
from property.models import Property
from user.models import Agent
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import QuerySet, Q, Count, When, Case, IntegerField, Value, OuterRef, Exists

class Room(Property):
    room_category = models.CharField(max_length=100, choices=ROOM_CATEGORY.choices(), default=ROOM_CATEGORY.default(), null=False, blank=False)
    
    class Meta:
        db_table = 'room'
        app_label = 'room'
        
    def delete(self) -> None:
        self.is_deleted = True
        self.save(update_fields=["is_deleted"], skip_validation=True)
        
    @classmethod
    def soft_delete_room(cls, property_id: uuid.UUID, agent: Agent) -> None:
        house = cls.objects.filter(property_id=property_id, agent=agent).first()
        
        if house is None:
            raise ValidationError(message="Mali haipo kwenye mfumo wetu")
        
        house.delete()
    
    @classmethod
    def save_room(cls, agent: Agent, location: Location, price: str, description: str, condition: str,
             nearby_facilities: str, utilities: str, security_features: str, heating_cooling_system: str,
             furnishing_status: str, room_category: str, rental_duration: str = None):
        """
        Save the Room instance and ensure all Property fields are passed and handled as parameters.
        
        Args:
            property_id (uuid.UUID): The unique identifier for the property.
            agent (Agent): The agent associated with the property.
            location (Location): The location of the property.
            price (Decimal): The price of the property.
            description (str): The description of the property.
            condition (str): The condition of the property.
            nearby_facilities (str): Nearby facilities to the property.
            utilities (str): Utilities available at the property.
            security_features (str): The security features of the property.
            heating_cooling_system (str): The heating/cooling system of the property.
            furnishing_status (str): The furnishing status of the property.
            room_category (str): The room category (e.g., 'Bedroom').
            rental_duration (str): Rental duration

        Returns:
            Room: The saved Room instance.
        """
        
        account = Account.get_account(agent=agent)
        
        if account is None:
            raise PermissionDenied("You don't have active account to uplaod room")
        
        if not account.can_upload(total_property=cls.total_properties_for_agent(agent=agent)):
            raise PermissionDenied("You have exceeded the maximum allowed properties.")
        
        if not ROOM_CATEGORY.valid(room_category=room_category):
            raise ValueError(f"Invalid room category: {room_category}.")
        

        instance = cls(
            agent=agent,
            location=location,
            category=CATEGORY.RENTAL.value,
            price=price,
            description=description,
            condition=condition,
            nearby_facilities=nearby_facilities,
            utilities=utilities,
            security_features=security_features,
            heating_cooling_system=heating_cooling_system,
            furnishing_status=furnishing_status,
            room_category=room_category,
            rental_duration=rental_duration,
        )

        instance.save()
        return instance
    
    @classmethod
    def get_room_by_id(cls, property_id: uuid.UUID) -> 'Room':
        """
        Class method to retrieve a room instance by its property ID.

        Args:
            property_id (uuid.UUID): The unique identifier for the property.

        Returns:
            Room or None: The room instance that matches the given property ID, or None if no match is found.
        """
        return cls.objects.filter(property_id=property_id, is_deleted = False).first()
    
    @classmethod
    def get_agent_room(cls, agent: Agent, property_id: uuid.UUID) -> 'Room':
        """Class method to retrieve the room for specific agent owning the room

        Args:
            agent (Agent): Agent inctance
            property_id (uuid.UUID): The unique identifier for the property

        Returns:
            Room or None: The room instance that matches the given property ID and agent, or None if no matches is found
        """
        return cls.objects.filter(agent=agent, property_id=property_id, is_deleted = False).first()
    
    @classmethod
    def get_agent_rooms(cls, agent: Agent) -> 'QuerySet[Room]':
        """Class method to retrieve all room property for specific agent

        Args:
            agent (Agent): Agent insatnce

        Returns:
            QuerySet[Room]: A queryset containing all rooms associated with the given agent.
        """
        return cls.objects.filter(agent=agent, is_deleted = False).order_by('-listing_date')
    
    @classmethod
    def get_rooms_with_no_images(cls, agent: Agent) -> 'QuerySet[Room]':
        """Class method to fetch rooms that have no images uploaded.

        Args:
            agent (Agent): Agent instance

        Returns:
            QuerySet[Room]: A queryset of rooms filtered based on the given criteria.
        """
        return cls.objects.filter(agent=agent, is_deleted = False).annotate(
            image_count = Count('images', distinct=True)
        ).filter(image_count = 0)
    
    @classmethod
    def room_filter(cls, region: str = None, district: str = None, min_price: Decimal = None, 
                    max_price: Decimal = None, room_category: str = None, ward: str = None, 
                    street: str = None) -> 'QuerySet[Room]':
        """
        Class method to filter rooms based on the given criteria.

        Args:
            region (str, optional): The region of the property. Defaults to None.
            district (str, optional): The district of the property. Defaults to None.
            min_price (Decimal, optional): The minimum price of the property. Defaults to None.
            max_price (Decimal, optional): The maximum price of the property. Defaults to None.
            room_category (str, optional): The category of the room (e.g., 'Bedroom'). Defaults to None.
            ward (str, optional): The ward of the property. Defaults to None.
            street (str, optional): The street of the property. Defaults to None.

        Returns:
            QuerySet[Room]: A queryset of rooms filtered based on the given criteria.
        """
        
        if room_category and not ROOM_CATEGORY.valid(room_category=room_category):
            raise ValueError(f"Invalid room category: {room_category}.")

        filters = Q(
            status=STATUS.AVAILABLE.value,
            is_active_account=True,
            category=CATEGORY.RENTAL.value,
            is_deleted = False
        )
        
        if room_category:
            filters &= Q(room_category=room_category)

        if min_price:
            filters &= Q(price__gte=min_price)

        if max_price:
            filters &= Q(price__lte=max_price)

        if region:
            filters &= Q(location__region__iexact=region)

        if district:
            filters &= Q(location__district__iexact=district)

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
