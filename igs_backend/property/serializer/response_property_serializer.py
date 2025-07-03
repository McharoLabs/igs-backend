from rest_framework import serializers

from house.models import House
from igs_backend.igs_backend import settings
from location.serializer.response_location_serializer import ResponseLocationSerializer
from property.models import Property
from room.models import Room


class ResponsePropertySerializer(serializers.ModelSerializer):
    location = ResponseLocationSerializer(many=False)
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['property_id', 'category', 'price', 'status', 'heating_cooling_system', 'rental_duration', 'description', 'condition', 'nearby_facilities', 'utilities', 
                  'security_features', 'furnishing_status', 'location', 'images']
    
    def get_images(self, obj):
        images = obj.images.all()
        image_urls = []

        base_url = settings.PROPERTY_IMAGE_BASE_URL 

        for image in images:
            image_id = image.image_id
            
            image_url = f"{base_url}/{image_id}/"
            
            image_urls.append(image_url)

        return image_urls
    

class ResponseDemoPropertySerializer(serializers.ModelSerializer):
    location = ResponseLocationSerializer(many=False)
    images = serializers.SerializerMethodField()
    is_active_account = serializers.BooleanField(write_only=True)
    agent = serializers.UUIDField(write_only=True)
    is_deleted = serializers.BooleanField(write_only=True)
    property_type = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = '__all__'

    def get_images(self, obj):
        """
        Generate full URLs for the images associated with this house in the desired format.
        """
        images = obj.images.all()
        image_urls = []

        base_url = settings.PROPERTY_IMAGE_BASE_URL 

        for image in images:
            image_id = image.image_id
            
            image_url = f"{base_url}/{image_id}/"
            
            image_urls.append(image_url)

        return image_urls
    
    def get_property_type(self, obj):
        """
        Returns the type of the property (House or Room)
        """
        if hasattr(obj, 'house'):
            return "House"
        elif hasattr(obj, 'room'):
            return "Room"
        return "Unknown"  


        