from rest_framework import serializers

from house.models import House
from house.serializer.response_room_serializer import ResponseRoomSerializer
from location.serializers import ResponseLocationSerializer

class ResponseHouseDetailSerializer(serializers.ModelSerializer):
    location = ResponseLocationSerializer(many=False)
    rooms = ResponseRoomSerializer(many=True)
    class Meta:
        model = House
        fields = '__all__'