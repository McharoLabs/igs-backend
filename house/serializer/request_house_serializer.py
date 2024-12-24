from rest_framework import serializers
from house.enums.category import CATEGORY
from house.enums.condition import CONDITION
from house.enums.heating_cooling_system import HEATING_COOLING_SYSTEM
from house.enums.furnishing_status import FURNISHING_STATUS
from house.enums.security_feature import SECURITY_FEATURES

class RequestHouseSerializer(serializers.Serializer):
    category = serializers.ChoiceField(choices=CATEGORY.choices(), required=True)
    title = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
    condition = serializers.ChoiceField(choices=CONDITION.choices(), required=True)
    nearby_facilities = serializers.CharField(required=True)
    utilities = serializers.CharField(required=True)
    security_features = serializers.ChoiceField(choices=SECURITY_FEATURES.choices(), required=True)
    heating_cooling_system = serializers.ChoiceField(choices=HEATING_COOLING_SYSTEM.choices(), required=True)
    furnishing_status = serializers.ChoiceField(choices=FURNISHING_STATUS.choices(), required=True)
    total_bed_room = serializers.IntegerField(required=True)
    total_dining_room = serializers.IntegerField(required=True)
    total_bath_room = serializers.IntegerField(required=True)
    district_id = serializers.UUIDField(required=True)
    ward = serializers.CharField(required=True, max_length=255)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
