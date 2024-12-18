from rest_framework import serializers

class DetailResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255)