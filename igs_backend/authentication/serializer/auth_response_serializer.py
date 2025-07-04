from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

class TokenResponseSerializer(serializers.Serializer):
    tokens = TokenSerializer()
