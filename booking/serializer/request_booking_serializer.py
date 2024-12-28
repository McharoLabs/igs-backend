from rest_framework import serializers

class RequestHouseBookingSerializer(serializers.Serializer):
    house_id = serializers.UUIDField(required=True)
    booking_fee = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
    
    
class RequestRoomBookingSerializer(serializers.Serializer):
    house_id = serializers.UUIDField(required=True)
    room_id = serializers.UUIDField(required=True)
    booking_fee = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
