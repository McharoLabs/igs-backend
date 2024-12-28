# serializers.py

from rest_framework import serializers

from booking.models import Booking

class PaymentResponseSerializer(serializers.Serializer):
    payment_id = serializers.UUIDField()  # Payment ID as a UUID
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.all())  # Link to booking
    amount = serializers.DecimalField(max_digits=32, decimal_places=2)  # Amount
    payment_date = serializers.DateTimeField()  # Payment date

    booking_description = serializers.CharField(source='booking.description', read_only=True)
