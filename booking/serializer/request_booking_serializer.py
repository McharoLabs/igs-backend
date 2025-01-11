from rest_framework import serializers

from utils.phone_number import validate_phone_number
    
class RequestBookingSerializer(serializers.Serializer):
    property_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(required=True)
