from rest_framework import serializers

from house.model.house_transaction import HouseTransaction
from house.serializer.respnse_house_serializer import ResponseHouseSerializer
from user.serializer.response_tenant_serializer import ResponseTenantSerializer

class ResponseTransactionSerailizer(serializers.ModelSerializer):
    tenant = ResponseTenantSerializer(many=False)
    house = ResponseHouseSerializer(many=False)
    class Meta:
        model = HouseTransaction
        fields = '__all__'