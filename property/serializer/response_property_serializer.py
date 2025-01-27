from rest_framework import serializers

from igs_backend import settings
from location.serializer.response_location_serializer import ResponseLocationSerializer
from property.models import Property


class ResponsePropertySerializer(serializers.ModelSerializer):
    location = ResponseLocationSerializer(many=False)
    images = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = ['property_id', 'category', 'price', 'description', 'condition', 'nearby_facilities', 'utilities', 
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
        