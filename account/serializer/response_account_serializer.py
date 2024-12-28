from rest_framework import serializers

from account.models import Account
from account.serializer.response_subscription_plan_serializer import ResponseSubscriptionPlanSerailizer

class ResponseAccountSerializer(serializers.ModelSerializer):
    plan = ResponseSubscriptionPlanSerailizer(many=False)
    class Meta:
        model = Account
        fields = '__all__'