from rest_framework import serializers
from house.models import House
from location.serializers import ResponseLocationSerializer
from django.conf import settings


class ResponseHouseSerializer(serializers.ModelSerializer):
    location = ResponseLocationSerializer(many=False)
    images = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = '__all__'

    def get_images(self, obj):
        """
        Generate full URLs for the images associated with this house in the desired format.
        """
        images = obj.house_image.all()
        image_urls = []

        base_url = settings.PROPERTY_IMAGE_BASE_URL 

        for image in images:
            image_id = image.image_id
            
            image_url = f"{base_url}/{image_id}/"
            
            image_urls.append(image_url)

        return image_urls
