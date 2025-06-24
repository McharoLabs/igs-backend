from rest_framework import serializers
from house.models import House

class RequestPropertyImageSerializer(serializers.Serializer):
    property_id = serializers.UUIDField(required=True)
    images = serializers.ListField(child=serializers.ImageField(), required=True)
