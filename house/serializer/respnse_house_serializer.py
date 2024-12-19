from rest_framework import serializers

from house.models import House
from location.serializers import ResponseLocationSerializer

class ResponseHouseSerializer(serializers.ModelSerializer):
    location = ResponseLocationSerializer(many=False)
    class Meta:
        model = House
        fields = '__all__'