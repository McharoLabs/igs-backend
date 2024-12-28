# serializers.py

import uuid
from rest_framework import serializers
from booking.models import Booking
from payment.models import Payment

class PaymentRequestSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()  # Booking ID as input
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)  # Payment amount
    payment_date = serializers.DateTimeField()  # Payment date

    def create(self, validated_data):
        # Manually handle creating a Payment instance
        booking = Booking.objects.get(id=validated_data['booking_id'])

        # Now create the Payment object
        payment = Payment.objects.create(
            booking=booking,
            amount=validated_data['amount'],
            payment_date=validated_data['payment_date']
        )
        return payment

    def update(self, instance: Payment, validated_data):
        # Manually handle updating a Payment instance
        booking = Booking.objects.get(id=validated_data['booking_id'])

        instance.booking = booking
        instance.amount = validated_data.get('amount', instance.amount)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)

        instance.save()
        return instance
