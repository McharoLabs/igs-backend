import uuid
from django.db import models

from location.model.location import Location
from user.model.agent import Agent
from user.model.landlord import LandLord
import logging
from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)

class House(models.Model):
    house_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name="houses")
    landlord = models.ForeignKey(LandLord, on_delete=models.SET_NULL, null=True, related_name="houses")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="houses")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_unit = models.CharField(max_length=50)
    condition = models.CharField(max_length=100)
    nearby_facilities = models.TextField()
    category = models.CharField(max_length=50)
    utilities = models.TextField()
    security_features = models.TextField()
    heating_cooling_system = models.CharField(max_length=255)
    furnishing_status = models.CharField(max_length=255)
    total_bed_room = models.IntegerField()
    total_dining_room = models.IntegerField()
    total_bath_room = models.IntegerField()
    total_floor = models.IntegerField()

    class Meta:
        db_table = 'house'
        
    def __str__(self) -> str:
        return self.title
    
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
        price_unit: str,
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
        total_floor: int,
        agent: Agent = None,
        landlord: LandLord = None
    ) -> str:
        """
        This method creates a new House and saves it to the database.

        Args:
            agent (Agent): Agent instance.
            landlord (LandLord): Landlord instance.
            location (Location): Location Instance.
            title (str): Title of the house.
            description (str): Description of the house.
            price_unit (str): Price unit for the house.
            condition (str): Condition of the house.
            nearby_facilities (str): Nearby facilities of the house.
            category (str): Category of the house.
            utilities (str): Utilities available at the house.
            security_features (str): Security features of the house.
            heating_cooling_system (str): Heating/cooling system in the house.
            furnishing_status (str): Furnishing status of the house.
            total_bed_room (int): Total number of bedrooms.
            total_dining_room (int): Total number of dining rooms.
            total_bath_room (int): Total number of bathrooms.
            total_floor (int): Total number of floors.

        Returns:
            str: Message indicating whether the house was successfully added.
        """
        
        house = cls(
            agent=agent,
            landlord=landlord,
            location=location,
            title=title,
            description=description,
            price_unit=price_unit,
            condition=condition,
            nearby_facilities=nearby_facilities,
            category=category,
            utilities=utilities,
            security_features=security_features,
            heating_cooling_system=heating_cooling_system,
            furnishing_status=furnishing_status,
            total_bed_room=total_bed_room,
            total_dining_room=total_dining_room,
            total_bath_room=total_bath_room,
            total_floor=total_floor
        )

        house.save()
        logger.info(f'House saved successfully: {house}')
        return f"House '{house.title}' added successfully"