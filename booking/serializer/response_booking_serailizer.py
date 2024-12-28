from rest_framework import serializers

from booking.models import Booking
from house.serializer.respnse_house_serializer import ResponseHouseSerializer
from house.serializer.response_room_serializer import ResponseRoomSerializer

class ResponseBookingSerailizer(serializers.ModelSerializer):
    house = ResponseHouseSerializer(many=False)
    room = ResponseRoomSerializer(many=False)
    class Meta:
        model = Booking
        fields = '__all__'