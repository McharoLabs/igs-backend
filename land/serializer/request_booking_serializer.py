from rest_framework import serializers
from utils.phone_number import validate_phone_number
    
class RequestLandAgentInfoSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100, required=True)
    customer_email = serializers.CharField(max_length=100, required=True)
    land_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(required=True, validators=[validate_phone_number])
