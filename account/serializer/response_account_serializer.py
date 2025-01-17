from rest_framework import serializers

from account.models import Account
from account.serializers import ResponseSubscriptionPlanSerailizer

class ResponseAccountSerializer(serializers.ModelSerializer):
    plan = ResponseSubscriptionPlanSerailizer(many=False)
    class Meta:
        model = Account
        fields = '__all__'