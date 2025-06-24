from rest_framework import serializers

class RequestDistrictSerializer(serializers.Serializer):
    district_name = serializers.CharField(max_length=100, required=True)
    region_id = serializers.UUIDField(required=True)