import io
import os
import tempfile
from typing import Any
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


def upload_image_to(instance, filename):
    image_id = instance.image_id 
    extension = filename.split('.')[-1]
    
    return os.path.join('property_images', str(image_id) + '.' + extension)
    

def upload_profile_to(instance, filename):
    user_id = instance.user_id 
    extension = filename.split('.')[-1]
    
    return os.path.join('avatar', str(user_id) + '.' + extension)

def validate_image(image):
    """Validates and compresses image before saving."""
    try:
        img = Image.open(image)
        img.verify()  # Check if it's a valid image file
    except Exception as e:
        raise ValidationError(message="Invalid image file.")

    return compress_and_resize_image(image)


def compress_and_resize_image(image: Any) -> InMemoryUploadedFile:
    """Resizes and compresses an image to optimize file size."""
    img = Image.open(image)
    max_width = 1920
    max_size_in_mb = 1.2

    if img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int((float(img.height) * float(ratio)))
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

    # Create a temporary file path
    temp_file_path = tempfile.mktemp(suffix=".webp")
    img.save(temp_file_path, format='WebP', quality=80)

    # Compress if the size is greater than the allowed limit
    while os.path.getsize(temp_file_path) > max_size_in_mb * 1024 * 1024:
        img.save(temp_file_path, format='WebP', quality=75)

    # Read the file into memory and create InMemoryUploadedFile
    with open(temp_file_path, 'rb') as f:
        img_data = f.read()
    
    # Use BytesIO to simulate the file in memory
    img_io = io.BytesIO(img_data)
    img_io.seek(0)

    # Create an InMemoryUploadedFile from the in-memory image
    compressed_image = InMemoryUploadedFile(
        img_io, None, temp_file_path, 'image/webp', len(img_data), None
    )

    # Clean up the temporary file
    os.remove(temp_file_path)

    return compressed_image
