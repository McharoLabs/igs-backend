from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from user.models import Agent

class RegisterUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    middle_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30)
    phone_number = serializers.CharField(max_length=15)
    gender = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True, max_length=255)
    avatar = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        password = validated_data.pop('password')

        validated_data['password'] = make_password(password)

        user = Agent.objects.create(**validated_data)

        return user
