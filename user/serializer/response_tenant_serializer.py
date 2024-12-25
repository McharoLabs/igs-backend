from rest_framework import serializers

from user.model.tenant import Tenant

class ResponseTenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ["user_id", "first_name", "middle_name", "last_name", "phone_number", "gender", "email", "avatar"]