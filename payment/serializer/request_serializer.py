from rest_framework import serializers

class RequestBookingPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=32, decimal_places=2, required=True)
    house_id = serializers.UUIDField(required=False)
    room_id = serializers.UUIDField(required=False)
    phone_number = serializers.CharField(required=True)
    

class RequestSubscriptionPaymentSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField(required=True)
    phone_number = serializers.CharField(required=True)