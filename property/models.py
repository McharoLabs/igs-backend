from typing import List
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

from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from utils.upload_image import upload_image_to, validate_image

class Property(models.Model):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.RESTRICT, null=False, related_name="properties")
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
    is_active_account = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    listing_date = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'property'
        app_label = 'property'

    def __str__(self):
        return f"Property {self.property_id}"
    
    def available(self) -> bool:
        return self.status == STATUS.AVAILABLE.value
    
    def mark_booked(self) -> None:
        self.status = STATUS.BOOKED.value
        self.save(update_fields=['status'])
    
    @classmethod
    def total_properties_for_agent(cls, agent: Agent) -> int:
        """Class method to calculate total properties for the specific agent

        Args:
            agent (Agent): Agent instance required to count the total properties

        Returns:
            int: Total number of properties
        """
        return cls.objects.filter(agent=agent).count()
    
    @classmethod
    def get_property_by_id(cls, property_id: uuid.UUID) -> 'Property | None':
        """Class method to retrieve property instance

        Args:
            property_id (uuid.UUID): Unique property id to retrieve the instance

        Returns:
            Property | None: Instance of property that matches the property ID if found, otherwise None
        """
        return cls.objects.filter(property_id=property_id).first()
    
    @classmethod
    def get_agent_property_by_id(cls, agent: Agent, property_id: uuid.UUID) -> 'Property | None':
        """Class method to retrieve property for the given agent and property ID

        Args:
            agent (Agent): Agent instance
            property_id (uuid.UUID): Unique property ID

        Returns:
            Property | None: Property instance that matches the criteria provided if found, Otherwise None
        """
        return cls.objects.filter(agent=agent, property_id=property_id).first()
    
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
        
        inactive_houses = cls.objects.filter(is_active_account=False, is_locked=False, status=STATUS.AVAILABLE.value, agent=agent)
        
        for house in inactive_houses:
            house.is_active_account = True
            house.save(update_fields=["is_active_account"])
            
    @classmethod
    def deactivate_active_properties(cls, agent: Agent):
        """
        Deactivates all inactive houses associated with the given agent.

        Args:
            agent (Agent, optional): The agent associated with the houses to activate.
        """
        inactive_houses = None
        
        inactive_houses = cls.objects.filter(is_active_account=True, is_locked=False, status=STATUS.AVAILABLE.value, agent=agent)
        
        for house in inactive_houses:
            house.is_active_account = False
            house.save(update_fields=["is_active_account"])
            

class PropertyImage(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_to, validators=[validate_image])
    
    class Meta:
        db_table = 'images'
        app_label = 'property'
    
    def __str__(self):
        return str(self.image_id)
    
    @classmethod
    def get_image_by_id(cls, image_id: uuid.UUID) -> 'PropertyImage':
        """Retrieve image instance using image id

        Args:
            image_id (uuid.UUID): Image id to retrieve the image instance

        Returns:
            PropertyImage: Image instance if found, otherwise None
        """
        return cls.objects.filter(image_id=image_id).first()
    
    @classmethod
    def save(cls, property: Property, images: List[InMemoryUploadedFile]) -> None:
        """Class method to save property images

        Args:
            property (Property): Property for which the images are uplaoded
            images (List[InMemoryUploadedFile]): List of images
        """
        image_objects = []
        
        for image in images:
            image_obj = cls(property=property, image=image)
            image_objects.append(image_obj)
            
        with transaction.atomic():
            cls.objects.bulk_create(image_objects)