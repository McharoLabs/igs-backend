from decimal import Decimal, InvalidOperation
import logging
import uuid
from django.db import models

from house.enums.category import CATEGORY
from house.enums.room_category import ROOM_CATEGORY
from house.enums.room_status import ROOM_STATUS
from django.db.models import QuerySet

from house.model.house import House
from django.db.models import Q

logger = logging.getLogger(__name__)

class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, related_name="rooms")
    room_category = models.CharField(max_length=100, choices=ROOM_CATEGORY.choices(), default=ROOM_CATEGORY.default(), null=False, blank=False)
    room_number = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=32, decimal_places=2, help_text="The price for the room")
    status = models.CharField(max_length=255, choices=ROOM_STATUS.choices(), default=ROOM_STATUS.default(), null=False, blank=False)

    class Meta:
        db_table = 'room'
        
    def update_room_status_to_booked(self) -> None:
        """Update the status of the room to 'booked'."""
        self.status = ROOM_STATUS.BOOKED.value
        self.save()
        
    @classmethod
    def get_room_by_house_and_room_number(cls, house: House, room_id: uuid.UUID) -> 'Room':
        """
        Retrieve a room by its associated house and room number.

        Args:
            house (House): The house to which the room belongs.
            room_id (uuid.UUID): The specific room id to find.

        Returns:
            Room: The room object if found, or None if no matching room exists.
        """
        return cls.objects.filter(house=house, room_id=room_id, status=ROOM_STATUS.AVAILABLE.value).first()

    @classmethod
    def has_rooms_for_house(cls, house: House) -> bool:
        """Check if a given house has rooms.

        Args:
            house (House): House instance used to check the rooms availability

        Returns:
            bool: True if any room exists for te house, otherwise false
        """
        return cls.objects.filter(house=house).exists()

    @classmethod
    def get_rooms_for_house(cls, house: House) -> 'QuerySet[Room]':
        """Get all rooms associated with a specific house.

        Args:
            house (House): House instance used to filter all the corresponding rooms 

        Returns:
            QuerySet[Room]: A list of room instance corresponding to the house, otherwise None
        """
        return cls.objects.filter(house=house)
    
    @classmethod
    def add_room(cls, house: House, room_category: str, room_number: str, price: Decimal) -> str:
        """Adds a new room to a specified house and returns a success message.

        This method creates a new room instance with the provided details (room category, room number, and price) 
        and associates it with the given house.

        Args:
            house (House): The house instance to which the room will be added.
            room_category (str): The category of the room (e.g., bedroom, living room, etc.).
            room_number (str): The number or identifier for the room (e.g., 'Room 1', 'Living Room').
            price (Decimal): The price of the room.

        Raises:
            ValueError: If the room category is invalid or if the price is not a valid decimal number.

        Returns:
            str: A success message indicating that the room was added successfully.
        """
        
        if room_category and not ROOM_CATEGORY.valid(room_category=room_category):
            raise ValueError(f"Invalid room category '{room_category}'. Value options are {', '.join(choice[0] for choice in ROOM_CATEGORY.choices())}")
        
        try:
            price_value = Decimal(price)
        except InvalidOperation:
            raise ValueError(f"Invalid price '{price}'. It must be a valid decimal number.")
        
        room = cls(
            house=house,
            room_category=room_category,
            room_number=room_number,
            price=price_value,
        )

        room.save()

        logger.info(f'Room saved successfully: {room}')

        return f"Room for '{house.title}' added successfully"
    
    @classmethod
    def filter_rooms(
        cls,
        region: str = None, 
        district: str = None,
        min_price: Decimal = None, 
        max_price: Decimal = None, 
        room_category: str = None
    ) -> 'QuerySet[Room]':
        """
        Filters rooms based on various parameters such as region, district, price range, and room category.

        Args:
            region (str, optional): The region of the house location to filter by. Defaults to None.
            district (str, optional): The district of the house location to filter by. Defaults to None.
            min_price (Decimal, optional): The minimum price of the room to filter by. Defaults to None.
            max_price (Decimal, optional): The maximum price of the room to filter by. Defaults to None.
            room_category (str, optional): The category of the room (e.g., bedroom, living room) to filter by. Defaults to None.

        Raises:
            ValueError: If an invalid `room_category` is provided, a ValueError is raised with an appropriate message.

        Returns:
            QuerySet[Room]: A queryset of rooms that match the provided filtering criteria.
        """
        
        if room_category and not ROOM_CATEGORY.valid(room_category=room_category):
            raise ValueError(f"Invalid room category '{room_category}'. Value options are {', '.join(choice[0] for choice in ROOM_CATEGORY.choices())}")

        filters = Q()
        filters &= Q(status=ROOM_STATUS.AVAILABLE.value)

        if room_category:
            filters &= Q(room_category=room_category)

        if min_price:
            filters &= Q(price__gte=min_price)

        if max_price:
            filters &= Q(price__lte=max_price)

        if region:
            filters &= Q(house__location__region__iexact=region)

        if district:
            filters &= Q(house__location__district__iexact=district)

        return cls.objects.filter(filters)