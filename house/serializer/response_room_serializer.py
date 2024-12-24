from rest_framework import serializers

from house.model.house_room import Room
from house.serializer.respnse_house_serializer import ResponseHouseSerializer

class ResponseRoomSerializer(serializers.ModelSerializer):
    house = ResponseHouseSerializer()
    
    class Meta:
        model = Room
        fields = '__all__'