import json
from django.http import HttpRequest
import requests
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from booking.models import Booking
from booking.serializers import  RequestBookingSerializer
from igs_backend import settings
from payment.enums.payment_type import PaymentType
from payment.models import Payment
from property.models import Property
from shared.seriaizers import DetailResponseSerializer
import logging
from django.core.exceptions import ValidationError

from utils.http_client import HttpClient




logger = logging.getLogger(__name__)

class BookingViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestBookingSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_actions = {'booked_rooms'}

        if self.action in agent_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Booking.objects.none()
    
    @swagger_auto_schema(
        operation_description="Make booking by providong necessary information such as property ID and tenant phoe number",
        operation_summary="Tenant booking",
        method="post",
        tags=["booking"],
        request_body=RequestBookingSerializer,
        responses={
            200: openapi.Response(
                description="Success",
                schema=DetailResponseSerializer(many=False),
            ),
            403: openapi.Response(
                description="Bad request, Property not available for booking",
                schema=DetailResponseSerializer(many=False)
            ),
            404: openapi.Response(
                description="Not found",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Bad request",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            ),
        },
    )
    @action(detail=False, methods=['post'])
    def make_booking(self, request: HttpRequest):
        request_serializer = RequestBookingSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        property = Property.get_property_for_booking(property_id=validated_data.get("property_id"))
        
        if not property:
            return Response(data={"detail": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

        if not property.available():
            return Response(data={"detail": "Property not available for booking"}, status=status.HTTP_403_FORBIDDEN)

        try:
            payment = Payment.create(
                phone_number=validated_data.get("phone_number"),
                payment_type=PaymentType.BOOKING,
                amount=settings.BOOKING_FEE,
                property=property,
            )
            
            phone_number = payment.phone_number
            if phone_number.startswith('+255'):
                phone_number = '0' + phone_number[4:]
            
            order_data = {
                    'buyer_email': validated_data.get('customer_email'),
                    'buyer_name': validated_data.get('customer_name'),
                    'buyer_phone': phone_number,
                    'amount': float(payment.amount),
                    'account_id': settings.ACCOUNT_ID,
                    'webhook_url': f"{settings.APP_BASE}{settings.WEB_HOOK_URL}",
                    'metadata': json.dumps({
                        'payment_id': str(payment.payment_id),
                        'customer_name': validated_data.get('customer_name'),
                        'customer_email': validated_data.get('customer_email'), 
                    }),
                    'api_key': settings.ZENOPAY_API_KEY,
                    'secret_key': settings.ZENOPAY_SECRET_KEY,
                }

            client = HttpClient(base_url=settings.ZENOPAY_BASE)
            response = client.make_payment(data=order_data)

            if response is None:
                return Response({"detail": "Payment gateway error, please try again later"}, status=status.HTTP_502_BAD_GATEWAY)

            logger.info(f"Booking payment for property {property} with payload: {json.dumps(order_data)} and response: {response.text}")

            if response.status_code == 200:
                response_data = response.json()
                response_status = response_data.get("status")

                if response_status.lower() == "error":
                    payment.delete() 
                    return Response(data={"detail": response_data.get("message")}, status=status.HTTP_400_BAD_REQUEST)

                payment.update_order_and_message(order_id=response_data.get("order_id"), message=response_data.get("message"))
                return Response(data={"detail": "Booking initiated. Please complete your payment to confirm your booking."}, status=status.HTTP_200_OK)

            payment.delete()
            return Response(data={"detail": "Unexpected error with payment gateway"}, status=status.HTTP_502_BAD_GATEWAY)

        except requests.Timeout as e:
            logger.error(f"Request timeout occurred: {e}", exc_info=True)
            payment.delete()
            return Response({"detail": "Payment request timed out. Please try again later."}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except requests.RequestException as e:
            logger.error(f"HTTP error occurred: {e}", exc_info=True)
            payment.delete()
            return Response({"detail": "Payment gateway error occurred. Please try again later."}, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            payment.delete()
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)