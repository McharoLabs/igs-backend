from rest_framework import serializers
from house.model.house_room import Room
from house.serializer.response_transaction_serailizer import ResponseTransactionSerailizer

class ResponseBookedRoomSerializer(serializers.ModelSerializer):
    booking = ResponseTransactionSerailizer(many=False, source='room_transactions.first')

    class Meta:
        model = Room
        fields = '__all__'
