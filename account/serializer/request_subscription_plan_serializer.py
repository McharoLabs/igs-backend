from rest_framework import serializers

class RequestSubscriptionPlanSerializer(serializers.Serializer):
    subscription_plan_id = serializers.UUIDField(required=True)