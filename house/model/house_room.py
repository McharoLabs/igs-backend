import logging
import uuid
from django.db import models

from house.enums.room_category import ROOM_CATEGORY
from house.enums.room_status import ROOM_STATUS
from django.db.models import QuerySet

from house.model.house import House

logger = logging.getLogger(__name__)

class Room(models.Model):
    room_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    house_id = models.ForeignKey(House, on_delete=models.SET_NULL, null=True, related_name="rooms")
    room_category = models.CharField(max_length=100, choices=ROOM_CATEGORY.choices(), default=ROOM_CATEGORY.default(), null=False, blank=False)
    room_number = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(max_digits=32, decimal_places=2, help_text="The price for the whoole house")
    status = models.CharField(max_length=255, choices=ROOM_STATUS.choices(), default=ROOM_STATUS.default(), null=False, blank=False)
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'room'

    @classmethod
    def has_rooms_for_house(cls, house_id: uuid.UUID) -> bool:
        """Check if a given house has rooms.

        Args:
            house_id (uuid.UUID): House id to check for the room existance

        Returns:
            bool: True if the house has any room, otherwise false
        """
        return cls.objects.filter(house_id=house_id).exists()

    @classmethod
    def get_rooms_for_house(cls, house_id: uuid.UUID) -> 'QuerySet[Room]':
        """Get all rooms associated with a specific house.

        Args:
            house_id (uuid.UUID): House id to find with all the associated rooms

        Returns:
            QuerySet[Room]: A list of room instances for the associated house
        """
        return cls.objects.filter(house_id=house_id)