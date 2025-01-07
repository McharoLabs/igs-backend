from decimal import Decimal
from typing import cast
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from house.enums.room_category import ROOM_CATEGORY
from house.models import Room, House
from house.serializers import RequestRoomSerializer, ResponseRoomDetailSerializer
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction

from user.model import User, Agent, LandLord


logger = logging.getLogger(__name__)

class RoomViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestRoomSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_room':
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return Room.objects.none()
    
    @swagger_auto_schema(
        operation_description="Add a new room for specific house by providing the necessary details such as house id, room number, price, etc.",
        operation_summary="Create New Room",
        method="post",
        tags=["Room"],
        request_body=RequestRoomSerializer,
        responses={200: DetailResponseSerializer(many=False), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['post'])
    @transaction.atomic(savepoint=False)
    def add_room(self, request: HttpRequest):
        user = cast(User, request.user)
        request_serializer = RequestRoomSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        landlord = LandLord.get_landlord_by_phone_number(phone_number=user.phone_number)
        agent = Agent.get_agent_by_phone_number(phone_number=user.phone_number)

        if landlord is None and agent is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:                
            house = House.get_house_by_agent_or_landlord(agent=agent, landlord=landlord, house_id=validated_data.get("house_id"))
            
            if house is None:
                return Response(data={"detail": "House not found"})
            
            response_message = Room.add_room(
                house=house, 
                room_category=validated_data.get("room_category"), 
                room_number=validated_data.get("room_number"), 
                price=validated_data.get("price")
            )

            response_serializer = DetailResponseSerializer({"detail": response_message})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @swagger_auto_schema(
        operation_description="List filtered rooms",
        operation_summary="Filtered Rooms",
        method="get",
        tags=["Room"],
        responses={
            200: openapi.Response(
                description="A paginated list of filtered rooms",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'next': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'room_id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'house': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'house_id': openapi.Schema(type=openapi.TYPE_STRING),
                                            'location': openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'location_id': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'region': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'district': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'ward': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'latitude': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'longitude': openapi.Schema(type=openapi.TYPE_STRING),
                                                }
                                            ),
                                            'images': openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(type=openapi.TYPE_STRING),
                                            ),
                                            'category': openapi.Schema(type=openapi.TYPE_STRING),
                                            'price': openapi.Schema(type=openapi.TYPE_STRING),
                                            'title': openapi.Schema(type=openapi.TYPE_STRING),
                                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                                            'condition': openapi.Schema(type=openapi.TYPE_STRING),
                                            'nearby_facilities': openapi.Schema(type=openapi.TYPE_STRING),
                                            'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                                            'security_features': openapi.Schema(type=openapi.TYPE_STRING),
                                            'heating_cooling_system': openapi.Schema(type=openapi.TYPE_STRING),
                                            'furnishing_status': openapi.Schema(type=openapi.TYPE_STRING),
                                            'total_bed_room': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'total_dining_room': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'total_bath_room': openapi.Schema(type=openapi.TYPE_INTEGER),
                                            'status': openapi.Schema(type=openapi.TYPE_STRING),
                                            'is_active_account': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                            'locked': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                            'is_full_house_rental': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                            'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                                            'agent': openapi.Schema(type=openapi.TYPE_STRING),
                                            'landlord': openapi.Schema(type=openapi.TYPE_STRING, nullable=True)
                                        }
                                    ),
                                    'room_category': openapi.Schema(type=openapi.TYPE_STRING),
                                    'room_number': openapi.Schema(type=openapi.TYPE_STRING),
                                    'price': openapi.Schema(type=openapi.TYPE_STRING),
                                    'status': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
                    }
                )
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
        manual_parameters=[
            openapi.Parameter(
                'region', openapi.IN_QUERY, description="Region of the house location", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'district', openapi.IN_QUERY, description="District of the house location", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'minPrice', openapi.IN_QUERY, description="Minimum price of the room", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'maxPrice', openapi.IN_QUERY, description="Maximum price of the room", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'roomCategory', openapi.IN_QUERY, 
                description="Category of the room (e.g., Self-contained, Shared, etc.)", 
                type=openapi.TYPE_STRING,
                enum=[category.value for category in ROOM_CATEGORY] 
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def filter_rooms(self, request: HttpRequest):
        
        region: str = request.GET.get('region')
        district: str = request.GET.get('district')
        min_price: str = request.GET.get('minPrice')
        max_price: str = request.GET.get('maxPrice')
        room_category: str = request.GET.get('roomCategory')
        
        try:
            min_price = Decimal(min_price) if min_price else None
            max_price = Decimal(max_price) if max_price else None
        except Exception as e:
            return Response({"detail": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rooms = Room.filter_rooms(region=region, district=district, min_price=min_price, max_price=max_price, room_category=room_category)
            
            paginator = PageNumberPagination()
            
            page = paginator.paginate_queryset(rooms, request)
            if page is not None:
                serializer = ResponseRoomDetailSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = ResponseRoomDetailSerializer(rooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
