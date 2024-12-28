import re
from rest_framework import serializers
from user.enums.gender import GENDER

class RequestLandLordRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30, required=True, min_length=1)
    middle_name = serializers.CharField(max_length=30, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=30, required=True, min_length=1)
    phone_number = serializers.CharField(max_length=15, required=True, min_length=1)
    gender = serializers.ChoiceField(choices=[(gender.value, gender.value) for gender in GENDER], required=True)
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=255, write_only=True, min_length=6)
    avatar = serializers.ImageField(required=False, allow_null=True)
    
    @classmethod
    def validate_phone_number(cls, value):
        """Method to validate a valid Tanzanian phone number format.

        This method checks that the phone number starts with the Tanzanian country code (+255)
        followed by 9 digits. If the phone number does not match this pattern, a 
        serializers.ValidationError is raised.

        Args:
            value (str): The phone number value to be validated. This value is provided by
                        the serializer and represents the phone number field input.

        Raises:
            serializers.ValidationError: If the phone number does not match the expected 
                                        Tanzanian format, a validation error is raised 
                                        with a custom error message.

        Returns:
            str: The validated phone number if it matches the required format.
        """
        pattern = r"^\+255\d{9}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid Tanzanian phone number. It should start with +255 and be followed by 9 digits.")
        return value

    

class ResponseLandLordRegistrationSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=255)
