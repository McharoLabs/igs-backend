from rest_framework import serializers

class RequestAccountSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField(required=True)