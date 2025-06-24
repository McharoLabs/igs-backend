from rest_framework import serializers

from location.models import Region

class ResponseRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'