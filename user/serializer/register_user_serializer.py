from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from user.enums.role_choice import ROLE_CHOICE
from user.models import Agent, Landlord, Tenant

class RegisterUserSerializer(serializers.Serializer):
    role = serializers.ChoiceField(choices=[(role.value, role.value) for role in ROLE_CHOICE])
    first_name = serializers.CharField(max_length=30)
    middle_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30)
    phone_number = serializers.CharField(max_length=15)
    gender = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True, max_length=255)
    avatar = serializers.ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        role = validated_data.pop('role')
        password = validated_data.pop('password')

        # Save the user based on the role
        validated_data['password'] = make_password(password)

        if role == 'Tenant':
            user = Tenant.objects.create(**validated_data)
        elif role == 'Landlord':
            user = Landlord.objects.create(**validated_data)
        elif role == 'Agent':
            user = Agent.objects.create(**validated_data)
        else:
            raise ValueError("Invalid role provided")

        return user
