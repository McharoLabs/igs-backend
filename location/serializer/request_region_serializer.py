import uuid
from rest_framework import serializers

class RequestRegionSerializer(serializers.Serializer):
    region_name = serializers.CharField(max_length=100, required=True)