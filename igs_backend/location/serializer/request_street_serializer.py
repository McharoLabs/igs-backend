from rest_framework import serializers

from location.models import Street

class RequestStreetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Street
        fields = '__all__'