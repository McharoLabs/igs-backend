from rest_framework import serializers

from location.models import District

class ResponseDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'