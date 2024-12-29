from rest_framework import serializers
    
class RequestBookingSerializer(serializers.Serializer):
    house_id = serializers.UUIDField(required=False)
    room_id = serializers.UUIDField(required=False)
    phone_number = serializers.CharField(required=True)
