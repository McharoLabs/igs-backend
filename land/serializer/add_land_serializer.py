from rest_framework import serializers

from land.enums.access_type import ACCESS_ROAD_TYPE
from land.enums.land_type import LAND_TYPE
from land.enums.zoning_type import ZONING_TYPE
from property.enums.rental_duration import RENTAL_DURATION

class AddLandSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
    rental_duration = serializers.ChoiceField(choices=RENTAL_DURATION.choices(), required=False, allow_null=True)
    category = serializers.ChoiceField(choices=LAND_TYPE.choices(), required=True)
    land_size = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    access_road_type = serializers.ChoiceField(choices=ACCESS_ROAD_TYPE.choices(), required=True)
    zoning_type = serializers.ChoiceField(choices=ZONING_TYPE.choices(), required=True)
    utilities = serializers.CharField(required=False, allow_blank=True)
    is_serviced = serializers.BooleanField(required=True)
    
    # Location fields
    district_id = serializers.UUIDField(required=True)
    ward = serializers.CharField(required=True, max_length=255)
    street = serializers.CharField(required=True, max_length=255)
    latitude = serializers.DecimalField(max_digits=11, decimal_places=8, required=False)
    longitude = serializers.DecimalField(max_digits=11, decimal_places=8, required=False)

    # Images
    images = serializers.ListField(child=serializers.ImageField(), required=True)
