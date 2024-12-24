from rest_framework import serializers

from house.enums.room_category import ROOM_CATEGORY

class RequestRoomSerializer(serializers.Serializer):
    house_id = serializers.UUIDField(required=True)
    room_category = serializers.ChoiceField(choices=ROOM_CATEGORY.choices(), required=True)
    room_number = serializers.CharField(max_length=255, required=True)
    price = serializers.DecimalField(max_digits=32, decimal_places=2, help_text="The price for the wholee house", required=True)
