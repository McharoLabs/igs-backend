import uuid
from django.db import models
from django.db import transaction
from django.core.files.uploadedfile import InMemoryUploadedFile
from typing import List
from house.model.house import House
from utils.upload_image import upload_image_to, validate_image

class PropertyImage(models.Model):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    house = models.ForeignKey(House, related_name='house_image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_to, validators=[validate_image])
    
    class Meta:
        db_table = 'property_image'
    
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
    def save_images(cls, house: House, images: List[InMemoryUploadedFile]) -> None:
        """
        Saves multiple image files associated with a specific house to the database.

        This method receives a list of image files, creates `PropertyImage` objects 
        for each of them, and then saves them to the database in bulk. This ensures 
        efficiency when saving many images at once.

        Args:
            house (House): The House instance that the images are associated with.
            images (list): A list of image files to be saved. Each item in the list should be 
                           an instance of `django.core.files.uploadedfile.InMemoryUploadedFile`
                           (the type of uploaded files in Django).

        Returns:
            None: This method does not return any value. It commits the transaction
                  and saves the images to the database.

        Example:
            house = House.objects.get(id=1)
            images = request.FILES.getlist('images')
            PropertyImage.save_images(house, images)
        """
        image_objects = []
        
        for image in images:
            image_obj = cls(house=house, image=image)
            image_objects.append(image_obj)
        
        with transaction.atomic():
            cls.objects.bulk_create(image_objects)
