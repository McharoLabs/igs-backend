from rest_framework import serializers

from igs_backend.igs_backend import settings
from land.models import Land
from location.serializers import ResponseLocationSerializer

class ResponseAgentLandSerializer(serializers.ModelSerializer):
    """
    Serializer for the AgentLand model.
    """
    location = ResponseLocationSerializer(many=False)
    images = serializers.SerializerMethodField()
    is_active_account = serializers.BooleanField(write_only=True)
    agent = serializers.UUIDField(write_only=True)
    is_deleted = serializers.BooleanField(write_only=True)

    class Meta:
        model = Land
        fields = '__all__'

    def get_images(self, obj):
        """
        Generate full URLs for the images associated with this Room in the desired format.
        """
        images = obj.images.all()
        image_urls = []

        base_url = settings.LAND_IMAGE_BASE_URL 

        for image in images:
            image_id = image.image_id
            
            image_url = f"{base_url}/{image_id}/"
            
            image_urls.append(image_url)

        return image_urls