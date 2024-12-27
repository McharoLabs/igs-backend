# serializers.py

from rest_framework import serializers
from house.model.house_transaction import HouseTransaction

class PaymentResponseSerializer(serializers.Serializer):
    payment_id = serializers.UUIDField()  # Payment ID as a UUID
    transaction = serializers.PrimaryKeyRelatedField(queryset=HouseTransaction.objects.all())  # Link to transaction
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)  # Amount
    payment_date = serializers.DateTimeField()  # Payment date

    transaction_description = serializers.CharField(source='transaction.description', read_only=True)
