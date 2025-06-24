from rest_framework import serializers

class RequestAvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=True)