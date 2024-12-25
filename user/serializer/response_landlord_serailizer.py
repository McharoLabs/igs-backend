from rest_framework import serializers

from user.model.landlord import LandLord


class ResponseLandLordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandLord
        fields = ["user_id", "first_name", "middle_name", "last_name", "phone_number", "gender", "email", "avatar"]