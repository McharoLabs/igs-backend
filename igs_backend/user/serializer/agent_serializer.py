import re
from rest_framework import serializers
from user.enums.gender import GENDER

class RequestAgentRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=True, min_length=1)
    middle_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=True, min_length=1)
    phone_number = serializers.CharField(max_length=10, required=True)
    gender = serializers.ChoiceField(choices=[(gender.value, gender.value) for gender in GENDER], required=True)
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=255, write_only=True, min_length=6)
    avatar = serializers.ImageField(required=True, allow_null=False)

    def validate_phone_number(self, value):
        """
        Validate that the phone number starts with '0' and has exactly 10 digits.
        """
        pattern = r"^0\d{9}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Invalid Tanzanian phone number. It must start with '0' and contain exactly 10 digits."
            )
        return value
