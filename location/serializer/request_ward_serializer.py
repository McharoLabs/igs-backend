from rest_framework import serializers

from location.models import Ward

class RequestWardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'