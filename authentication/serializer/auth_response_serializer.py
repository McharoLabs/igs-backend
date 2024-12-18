from rest_framework import serializers

class AuthResponse(serializers.Serializer):
    access = serializers.CharField(max_length=512)
    refresh = serializers.CharField(max_length=512) 