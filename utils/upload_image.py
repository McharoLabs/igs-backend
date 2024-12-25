import os
from PIL import Image
from django.core.exceptions import ValidationError


def upload_image_to(instance, filename):
    image_id = instance.image_id 
    extension = filename.split('.')[-1]
    
    return os.path.join('property_images', str(image_id) + '.' + extension)


def validate_image(image):
    try:
        img = Image.open(image)
        img.verify()
    except Exception as e:
        raise ValidationError("Invalid image file.")
    

def upload_profile_to(instance, filename):
    user_id = instance.user_id 
    extension = filename.split('.')[-1]
    
    return os.path.join('avatar', str(user_id) + '.' + extension)