# serializers.py

import uuid
from rest_framework import serializers
from payment.models import Payment
from user.models import Tenant
from house.model.house_transaction import HouseTransaction

class PaymentRequestSerializer(serializers.Serializer):
    tenant_id = serializers.IntegerField()  # Tenant ID as input
    transaction_id = serializers.IntegerField()  # Transaction ID as input
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)  # Payment amount
    payment_date = serializers.DateTimeField()  # Payment date

    def create(self, validated_data):
        # Manually handle creating a Payment instance
        tenant = Tenant.objects.get(id=validated_data['tenant_id'])
        transaction = HouseTransaction.objects.get(id=validated_data['transaction_id'])

        # Now create the Payment object
        payment = Payment.objects.create(
            tenant=tenant,
            transaction=transaction,
            amount=validated_data['amount'],
            payment_date=validated_data['payment_date']
        )
        return payment

    def update(self, instance: Payment, validated_data):
        # Manually handle updating a Payment instance
        tenant = Tenant.objects.get(id=validated_data['tenant_id'])
        transaction = HouseTransaction.objects.get(id=validated_data['transaction_id'])

        instance.tenant = tenant
        instance.transaction = transaction
        instance.amount = validated_data.get('amount', instance.amount)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)

        instance.save()
        return instance
