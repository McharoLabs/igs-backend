from rest_framework import serializers

class RequestSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(required=True)