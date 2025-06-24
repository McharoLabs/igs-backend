from rest_framework import serializers

from account.models import Account
from subscription_plan.models import SubscriptionPlan

class ResponseSubscriptionPlanSerailizer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'

class ResponseAccountSerializer(serializers.ModelSerializer):
    plan = ResponseSubscriptionPlanSerailizer(many=False)
    class Meta:
        model = Account
        fields = '__all__'