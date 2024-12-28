from rest_framework import serializers

from account.models import SubscriptionPlan

class ResponseSubscriptionPlanSerailizer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'