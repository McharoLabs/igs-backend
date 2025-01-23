from rest_framework import serializers

from utils.phone_number import validate_phone_number
    
class RequestBookingSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=100, required=True)
    customer_email = serializers.CharField(max_length=100, required=True)
    property_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(required=True)
