# serializers.py

from rest_framework import serializers
from user.models import Tenant
from house.model.house_transaction import HouseTransaction

class PaymentResponseSerializer(serializers.Serializer):
    payment_id = serializers.UUIDField()  # Payment ID as a UUID
    tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all())  # Link to tenant
    transaction = serializers.PrimaryKeyRelatedField(queryset=HouseTransaction.objects.all())  # Link to transaction
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)  # Amount
    payment_date = serializers.DateTimeField()  # Payment date

    tenant_name = serializers.CharField(source='tenant.first_name', read_only=True)
    transaction_description = serializers.CharField(source='transaction.description', read_only=True)
