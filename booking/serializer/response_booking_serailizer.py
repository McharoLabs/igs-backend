from rest_framework import serializers

from booking.models import Booking
from property.serializers import ResponsePropertySerializer

class ResponseBookingSerailizer(serializers.ModelSerializer):
    property = ResponsePropertySerializer(many=False)
    class Meta:
        model = Booking
        fields = '__all__'