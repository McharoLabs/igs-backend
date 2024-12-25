from rest_framework import serializers

from house.model.house_transaction import HouseTransaction
from house.serializer.respnse_house_serializer import ResponseHouseSerializer
from house.serializer.response_room_serializer import ResponseRoomSerializer
from user.serializer.response_tenant_serializer import ResponseTenantSerializer

class ResponseBookingSerailizer(serializers.ModelSerializer):
    tenant = ResponseTenantSerializer(many=False)
    house = ResponseHouseSerializer(many=False)
    room = ResponseRoomSerializer(many=False)
    class Meta:
        model = HouseTransaction
        fields = '__all__'