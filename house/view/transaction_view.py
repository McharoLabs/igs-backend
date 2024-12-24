from decimal import Decimal
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from house.enums.room_category import ROOM_CATEGORY
from house.models import Room, House, HouseTransaction
from house.serializers import RequestHouseTransactionSerializer, RequestRoomTransactionSerializer
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction


logger = logging.getLogger(__name__)

class HouseTransactionViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestHouseTransactionSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'house_booking' or self.action == 'room_booking':
            permission_classes = [permissions.IsAuthenticated, IsTenant]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return HouseTransaction.objects.none()
    
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
            amount = Decimal(validated_data.get("amount"))
        except Exception as e:
            return Response({"detail": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():               
                response_message = HouseTransaction.save_booking(
                    house=house,
                    tenant=tenant,
                    amount=amount
                )
                
                house.update_house_availability()
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
            return Response(data={"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
        
        room = Room.get_room_by_house_and_room_number(house=house, room_id=validated_data.get("room_id"))
        
        if room is None:
            return Response(data={"detail": f"Room for {house.title} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            amount = Decimal(validated_data.get("amount"))
        except Exception as e:
            return Response({"detail": "Invalid amount format."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():               
                response_message = HouseTransaction.save_booking(
                    house=house,
                    tenant=tenant,
                    amount=amount,
                    room=room
                )
                
                room.update_room_status_to_booked()
                
                response_serializer = DetailResponseSerializer({"detail": response_message})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    # @swagger_auto_schema(
    #     operation_description="List filtered rooms",
    #     operation_summary="Filtered Rooms",
    #     method="get",
    #     tags=["Rooms"],
    #     responses={200: ResponseRoomDetailSerializer(many=True)},
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'region', openapi.IN_QUERY, description="Region of the house location", type=openapi.TYPE_STRING
    #         ),
    #         openapi.Parameter(
    #             'district', openapi.IN_QUERY, description="District of the house location", type=openapi.TYPE_STRING
    #         ),
    #         openapi.Parameter(
    #             'minPrice', openapi.IN_QUERY, description="Minimum price of the room", type=openapi.TYPE_STRING
    #         ),
    #         openapi.Parameter(
    #             'maxPrice', openapi.IN_QUERY, description="Maximum price of the room", type=openapi.TYPE_STRING
    #         ),
    #         openapi.Parameter(
    #             'roomCategory', openapi.IN_QUERY, 
    #             description="Category of the room (e.g., Self-contained, Shared, etc.)", 
    #             type=openapi.TYPE_STRING,
    #             enum=[category.value for category in ROOM_CATEGORY] 
    #         ),
    #     ]
    # )
    # @action(detail=False, methods=['get'])
    # def filter_rooms(self, request):
        
    #     region: str = request.query_params.get('region')
    #     district: str = request.query_params.get('district')
    #     min_price: str = request.query_params.get('minPrice')
    #     max_price: str = request.query_params.get('maxPrice')
    #     room_category: str = request.query_params.get('roomCategory')
        
    #     try:
    #         min_price = Decimal(min_price) if min_price else None
    #         max_price = Decimal(max_price) if max_price else None
    #     except Exception as e:
    #         return Response({"detail": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         rooms = Room.filter_rooms(region=region, district=district, min_price=min_price, max_price=max_price, room_category=room_category)
            
    #         paginator = PageNumberPagination()
            
    #         page = paginator.paginate_queryset(rooms, request)
    #         if page is not None:
    #             serializer = ResponseRoomDetailSerializer(page, many=True)
    #             return paginator.get_paginated_response(serializer.data)

    #         serializer = ResponseRoomDetailSerializer(rooms, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except ValueError as e:
    #         logger.error(f"Validation error occurred: {e}", exc_info=True)
    #         return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         logger.error(f"Unexpected error occurred: {e}", exc_info=True)
    #         return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
