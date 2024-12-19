from rest_framework import serializers

from house.enums.category import CATEGORY

class RequestHouseSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=[(choice.value, choice.name) for choice in CATEGORY], required=True)
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    price_unit = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
    condition = serializers.CharField(max_length=100, required=True)
    nearby_facilities = serializers.CharField(required=True)
    utilities = serializers.CharField(required=True)
    security_features = serializers.CharField(required=True)
    heating_cooling_system = serializers.CharField(max_length=255, required=True)
    furnishing_status = serializers.CharField(max_length=255, required=True)
    total_bed_room = serializers.IntegerField(required=True)
    total_dining_room = serializers.IntegerField(required=True)
    total_bath_room = serializers.IntegerField(required=True)
    total_floor = serializers.IntegerField(required=True)
    district_id = serializers.UUIDField(required=True)
    ward = serializers.CharField(max_length=255)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6)
