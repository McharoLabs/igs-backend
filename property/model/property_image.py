import uuid
from django.db import models
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import List
from property.model.property import Property
from utils.upload_image import upload_image_to, validate_image

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