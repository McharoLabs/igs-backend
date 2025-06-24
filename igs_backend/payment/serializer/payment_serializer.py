from rest_framework import serializers

class PaymentSerializer(serializers.Serializer):
    order_id = serializers.CharField(max_length=255)
    payment_status = serializers.CharField(max_length=255)
    reference = serializers.CharField(max_length=255)