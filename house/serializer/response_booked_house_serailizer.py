from rest_framework import serializers
from house.model.house import House
from house.serializer.response_transaction_serailizer import ResponseTransactionSerailizer
from user.serializer.response_agent_serializer import ResponseAgentSerializer
from user.serializer.response_landlord_serailizer import ResponseLandLordSerializer

class ResponseBookedHouseSerializer(serializers.ModelSerializer):
    agent = ResponseAgentSerializer(many=False)
    landlord = ResponseLandLordSerializer(many=False)
    booking = ResponseTransactionSerailizer(many=False, source='house_transactions.first')

    class Meta:
        model = House
        fields = '__all__'
