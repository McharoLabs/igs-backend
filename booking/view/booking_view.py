from decimal import Decimal
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from booking.models import Booking
from booking.serializers import RequestHouseBookingSerializer, ResponseBookingSerailizer, RequestRoomBookingSerializer
from house.models import House, Room
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.core.exceptions import ValidationError

from user.models import LandLord, Agent



logger = logging.getLogger(__name__)

class BookingViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestHouseBookingSerializer

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
    
    @swagger_auto_schema(
        operation_description="Boking house by providing necessary details such as amount, house_id etc",
        operation_summary="House Booking",
        method="post",
        tags=["Booking"],
        request_body=RequestHouseBookingSerializer,
        responses={
            200: DetailResponseSerializer(many=False),
            201: "Data saved to database",
            400: "Invalid data",
            401: "Unauthorized",
            403: "Forbiden",
            404: "Not found",
            500: "Internal server error"
        },
    )
    @action(detail=False, methods=['post'])
    @transaction.atomic(savepoint=False)
    def house_booking(self, request: HttpRequest):
        request_serializer = RequestHouseBookingSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        user = request.user
        if not user.is_authenticated:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        house = House.get_house_by_id(house_id=validated_data.get("house_id"))
        
        if house is None:
            return Response(data={"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_fee = Decimal(validated_data.get("booking_fee"))
        except Exception as e:
            return Response({"detail": "Invalid booking fee format."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():               
                response_message = Booking.save_booking(
                    house=house,
                    booking_fee=booking_fee
                )
                
                house.update_status_to_booked()
                response_serializer = DetailResponseSerializer({"detail": response_message})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Boking room by providing necessary details such as amount, room number, house_id, etc",
        operation_summary="House Booking",
        method="post",
        tags=["Booking"],
        request_body=RequestRoomBookingSerializer,
        responses={
            200: DetailResponseSerializer(many=False),
            201: "Data saved to database",
            400: "Invalid data",
            401: "Unauthorized",
            403: "Forbiden",
            404: "Not found",
            500: "Internal server error"
        },
    )
    @action(detail=False, methods=['post'])
    @transaction.atomic(savepoint=False)
    def room_booking(self, request: HttpRequest):
        request_serializer = RequestRoomBookingSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        user = request.user
        if not user.is_authenticated:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        house = House.get_house_by_id(house_id=validated_data.get("house_id"))
        
        if house is None:
            return Response(data={"detail": "House not available for booking"}, status=status.HTTP_404_NOT_FOUND)
        
        room = Room.get_room_by_house_and_room_number(house=house, room_id=validated_data.get("room_id"))
        
        if room is None:
            return Response(data={"detail": f"Room not available for booking"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_fee = Decimal(validated_data.get("booking_fee"))
        except Exception as e:
            return Response({"detail": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():               
                response_message = Booking.save_booking(
                    house=house,
                    booking_fee=booking_fee,
                    room=room
                )
                
                room.update_status_to_booked()
                
                response_serializer = DetailResponseSerializer({"detail": response_message})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
