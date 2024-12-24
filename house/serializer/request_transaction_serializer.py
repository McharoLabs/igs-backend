from rest_framework import serializers

from house.enums.transaction_type import TRANSACTION_TYPE

class RequestHouseTransactionSerializer(serializers.Serializer):
    house_id = serializers.UUIDField(required=True)
    amount = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
    
    
class RequestRoomTransactionSerializer(serializers.Serializer):
    house_id = serializers.UUIDField(required=True)
    room_id = serializers.UUIDField(required=True)
    amount = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
