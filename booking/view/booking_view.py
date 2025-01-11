from django.http import HttpRequest
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
        tags=["Booking"],
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
        
        property = Property.get_property_by_id(property_id=validated_data.get("property_id"))
        
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
            
            return Response(data={"detail": "You have initiated payment for booking, please finish your payment"}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e.message}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)