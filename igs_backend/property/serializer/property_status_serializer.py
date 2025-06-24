from rest_framework import serializers

class RequestPropertyStatusSerializer(serializers.Serializer):
    property_id = serializers.UUIDField(required=True)