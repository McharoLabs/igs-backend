from decimal import Decimal
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from house.models import Room, House, HouseTransaction
from house.serializers import RequestHouseTransactionSerializer, RequestRoomTransactionSerializer, ResponseBookingSerailizer
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)

class HouseTransactionViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestHouseTransactionSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        tenant_actions = {'house_booking', 'room_booking', 'tenant_house_bookings', 'tenant_room_bookings'}
        agent_landlord_actions = {'booked_houses', 'booked_rooms'}

        if self.action in tenant_actions:
            permission_classes = [permissions.IsAuthenticated, IsTenant]
        elif self.action in agent_landlord_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return HouseTransaction.objects.none()
    
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
        landlord = LandLord.get_landlord_by_username(username=request.user)
        agent = Agent.get_agent_by_username(username=request.user)

        if landlord is None and agent is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
          bookings = HouseTransaction.get_booked_owner_house(agent=agent, landlord=landlord)
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
        landlord = LandLord.get_landlord_by_username(username=request.user)
        agent = Agent.get_agent_by_username(username=request.user)

        if landlord is None and agent is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
          bookings = HouseTransaction.get_booked_owner_room(agent=agent, landlord=landlord)
          response_serializer = ResponseBookingSerailizer(bookings, many=True)
          return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Retrieve booked rooms for the authenticated tenant.",
        operation_summary="Retrieve Tenant Room Bookings",
        method="get",
        tags=["Booking"],
        responses={200: ResponseBookingSerailizer(many=True), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['get'])
    def tenant_room_bookings(self, request):
        """Custom action to retrieve booked rooms for tenant."""
        tenant = Tenant.get_tenant_by_username(username=request.user)

        if tenant is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
          bookings = HouseTransaction.get_booked_tenant_room(tenant=tenant)
          response_serializer = ResponseBookingSerailizer(bookings, many=True)
          return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Retrieve booked house for the authenticated tenant.",
        operation_summary="Retrieve Tenant House Bookings",
        method="get",
        tags=["Booking"],
        responses={200: ResponseBookingSerailizer(many=True), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['get'])
    def tenant_house_bookings(self, request):
        """Custom action to retrieve booked house for tenant."""
        tenant = Tenant.get_tenant_by_username(username=request.user)

        if tenant is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
          bookings = HouseTransaction.get_booked_tenant_house(tenant=tenant)
          response_serializer = ResponseBookingSerailizer(bookings, many=True)
          return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Boking house by providing necessary details such as amount, house_id, the tenant_id etc",
        operation_summary="House Booking",
        method="post",
        tags=["Booking"],
        request_body=RequestHouseTransactionSerializer,
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
        request_serializer = RequestHouseTransactionSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        user = request.user
        if not user.is_authenticated:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        tenant = Tenant.get_by_username(username=user.username)
        
        house = House.get_house_by_id(house_id=validated_data.get("house_id"))
        
        if house is None:
            return Response(data={"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            booking_fee = Decimal(validated_data.get("booking_fee"))
        except Exception as e:
            return Response({"detail": "Invalid booking fee format."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():               
                response_message = HouseTransaction.save_booking(
                    house=house,
                    tenant=tenant,
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
        operation_description="Boking room by providing necessary details such as amount, room number, house_id, tenant_id etc",
        operation_summary="House Booking",
        method="post",
        tags=["Booking"],
        request_body=RequestRoomTransactionSerializer,
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
        request_serializer = RequestRoomTransactionSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        user = request.user
        if not user.is_authenticated:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        tenant = Tenant.get_by_username(username=user.username)
        
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
                response_message = HouseTransaction.save_booking(
                    house=house,
                    tenant=tenant,
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
