from decimal import Decimal
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from booking.models import Booking
from booking.serializers import  ResponseBookingSerailizer, RequestBookingSerializer
from house.models import House, Room
from igs_backend import settings
from payment.enums.payment_type import PaymentType
from payment.models import Payment
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.core.exceptions import ValidationError

from user.models import LandLord, Agent



logger = logging.getLogger(__name__)

class BookingViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestBookingSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_landlord_actions = {'booked_houses', 'booked_rooms'}

        if self.action in agent_landlord_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Booking.objects.none()
    
    @swagger_auto_schema(
        operation_description="Make booking by providing house id, room id of the tenant need to book room and phone number of the tenant",
        operation_summary="Tenant booking",
        method="post",
        tags=["Booking"],
        request_body=RequestBookingSerializer,
        responses={
            200: DetailResponseSerializer(many=True),
            400: "Invalid input data"
        },
    )
    @action(detail=False, methods=['post'])
    def make_booking(self, request: HttpRequest):
        request_serializer = RequestBookingSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        house = House.get_house_by_id(house_id=validated_data.get("house_id"))
        room = Room.get_room(room_id=validated_data.get("room_id"))
        
        if house is None:
            return Response(data={"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
        
        room = None
        if validated_data.get("room_id") is not None:
            room = Room.get_room(room_id=validated_data.get("room_id"))
            
            if room is None:
                return Response(data={"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
            
        if room is None and not house.is_full_house_rental:
            return Response(data={"detail": "The house rents room individual, room required"})
        
        try:
            payment = Payment.create_payment(
                phone_number=validated_data.get("phone_number"), 
                payment_type=PaymentType.BOOKING, 
                amount=settings.BOOKING_FEE, 
                house=house,
                room=room,
            )
            
            return Response(data={"detail": "You have initiated payment for booking, please finish your payment"}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Retrieve booked houses for the authenticated agent or landlord.",
        operation_summary="Retrieve Agent or Landlord Booked Houses",
        method="get",
        tags=["Booking"],
        responses={200: ResponseBookingSerailizer(many=True), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['get'])
    def booked_houses(self, request):
        """Custom action to retrieve booked houses for an agent or landlord."""
        landlord = LandLord.get_landlord_by_phone_number(phone_number=request.user)
        agent = Agent.get_agent_by_phone_number(phone_number=request.user)

        if landlord is None and agent is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
          bookings = Booking.get_booked_owner_houses(agent=agent, landlord=landlord)
          response_serializer = ResponseBookingSerailizer(bookings, many=True)
          return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Retrieve booked rooms for the authenticated agent or landlord.",
        operation_summary="Retrieve Agent or Landlord Booked Rooms",
        method="get",
        tags=["Booking"],
        responses={200: ResponseBookingSerailizer(many=True), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['get'])
    def booked_rooms(self, request):
        """Custom action to retrieve booked rooms for an agent or landlord."""
        landlord = LandLord.get_landlord_by_phone_number(phone_number=request.user)
        agent = Agent.get_agent_by_phone_number(phone_number=request.user)

        if landlord is None and agent is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
          bookings = Booking.get_booked_owner_rooms(agent=agent, landlord=landlord)
          response_serializer = ResponseBookingSerailizer(bookings, many=True)
          return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
