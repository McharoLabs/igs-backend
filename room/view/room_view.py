from decimal import Decimal
from typing import cast
import uuid
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from house.enums.room_category import ROOM_CATEGORY
from location.models import District
from location.models import Location
from property.models import Property
from property_images.models import PropertyImage
from room.models import Room
from room.serializers import RequestRoomSerializer, ResponseRoomSerializer, ResponseMyRoomSerializer
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction, DatabaseError
from django.core.exceptions import PermissionDenied, ValidationError

from user.enums.gender import GENDER
from user.models import Agent
from user.models import User

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


logger = logging.getLogger(__name__)

@method_decorator(never_cache, name='dispatch')
class RoomViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestRoomSerializer
    
    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_room' or self.action == 'room_list' or self.action == 'retrieve_room':
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return Room.objects.none()
    
    @swagger_auto_schema(
        operation_description="Add a new room by providing the necessary details such as agent, location, price, etc.",
        operation_summary="Create New Room",
        method="post",
        tags=["room"],
        request_body=RequestRoomSerializer,
        responses={
            201: openapi.Response(
                description="House property added successful",
                schema=DetailResponseSerializer(many=False)
            ), 
            404: openapi.Response(
                description="District not found",
                schema=DetailResponseSerializer(many=False)
            ), 
            401: openapi.Response(
                description="Unauthorized, agent not recognized",
                schema=DetailResponseSerializer(many=False)
            ),
            403: openapi.Response(
                description="Forbidden",
                schema=DetailResponseSerializer(many=False)
            ),
            404: openapi.Response(
                description="Bad request",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            )
        },
    )
    @action(detail=False, methods=['post'])
    @transaction.atomic(savepoint=False)
    def add_room(self, request: HttpRequest): 
        user = cast(User, request.user)      
        request_serializer = RequestRoomSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data


        try:
            district: District | None = District.get_district_by_id(district_id=validated_data.get("district_id"))
            
            if district is None:
                return Response(data={"detail": "District not found"}, status=status.HTTP_404_NOT_FOUND)

            agent: Agent | None = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
            
            if agent is None:
                return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
            
            with transaction.atomic():
                location = Location.add_location(
                    region=district.region.name,
                    district=district.name,
                    ward=validated_data.get("ward"),
                    latitude=validated_data.get("latitude"),
                    longitude=validated_data.get("longitude")
                )

                response = Room.save_room(
                    location=location, 
                    description=validated_data.get("description"), 
                    price=validated_data.get("price"), 
                    condition=validated_data.get("condition"), 
                    nearby_facilities=validated_data.get("nearby_facilities"),
                    utilities=validated_data.get("utilities"),
                    security_features=validated_data.get("security_features"),
                    heating_cooling_system=validated_data.get("heating_cooling_system"),
                    furnishing_status=validated_data.get("furnishing_status"),
                    room_category=validated_data.get("room_category"),
                    rental_duration=validated_data.get("rental_duration"),
                    agent=agent
                )
                
                property = Property.get_property_by_id(property_id=response.property_id)
                
                PropertyImage.save(property=property, images=validated_data.get("images"))

                response_serializer = DetailResponseSerializer({"detail": "Room uploaded successful"})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}", exc_info=True)
            error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or e
            return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied as e:
            logger.warning(f"Permission error: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except DatabaseError as e:
            logger.critical(f"Database error: {e}", exc_info=True)
            return Response({"detail": "A database error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="List all rooms",
        operation_summary="List Room",
        method="get",
        tags=["room"],
        responses={
            200: openapi.Response(
                description="A paginated list of rooms",
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
                                    'room_category': openapi.Schema(type=openapi.TYPE_STRING),
                                    'price': openapi.Schema(type=openapi.TYPE_STRING),
                                    'rental_duration': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'condition': openapi.Schema(type=openapi.TYPE_STRING),
                                    'nearby_facilities': openapi.Schema(type=openapi.TYPE_STRING),
                                    'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                                    'security_features': openapi.Schema(type=openapi.TYPE_STRING),
                                    'heating_cooling_system': openapi.Schema(type=openapi.TYPE_STRING),
                                    'furnishing_status': openapi.Schema(type=openapi.TYPE_STRING),
                                    'is_locked': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        )
                    }
                ),
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
        }
    )
    @action(detail=False, methods=['get'])
    def room_list(self, request: HttpRequest):
        user = cast(User, request.user)
        
        try:
            agent = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
            
            if agent is None:
                return Response(data={"detail": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
            
            houses = Room.get_agent_rooms(agent=agent)
            
            paginator = PageNumberPagination()
            page = paginator.paginate_queryset(houses, request)

            if page is not None:
                serializer = ResponseMyRoomSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = ResponseMyRoomSerializer(houses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except PermissionDenied as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
    @swagger_auto_schema(
        operation_description="Retrieve a room by property ID and agent",
        operation_summary="Retrieve Agent Room",
        method="get",
        tags=["room"],
        responses={
            200: openapi.Response(
                description="Retrieve a room",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'property_id': openapi.Schema(type=openapi.TYPE_STRING),
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
                        'room_category': openapi.Schema(type=openapi.TYPE_STRING),
                        'price': openapi.Schema(type=openapi.TYPE_STRING),
                        'rental_duration': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'condition': openapi.Schema(type=openapi.TYPE_STRING),
                        'nearby_facilities': openapi.Schema(type=openapi.TYPE_STRING),
                        'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                        'security_features': openapi.Schema(type=openapi.TYPE_STRING),
                        'heating_cooling_system': openapi.Schema(type=openapi.TYPE_STRING),
                        'furnishing_status': openapi.Schema(type=openapi.TYPE_STRING),
                        'is_locked': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
            404: openapi.Response(
                description="Not found",
                schema=DetailResponseSerializer(many=False)
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal serevr error",
                schema=DetailResponseSerializer(many=False)
            ),
        },
    )
    @action(detail=True, methods=['get'])
    def retrieve_room(self, request: HttpRequest, pk: uuid.UUID=None):
        """Retrieve a specific room by ID."""
        try:
            user = cast(User, request.user)
            agent: Agent = None

            if hasattr(user, 'agent'):
                agent = cast(Agent, user)
            else:
                return Response(data={"detail": "You are not authorized to view this resource"}, status=status.HTTP_401_UNAUTHORIZED)
            
            room = Room.get_agent_room(agent=agent, property_id=pk)
            
            if not room:
                return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResponseMyRoomSerializer(room, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
          logger.error(f"Un expected error occured while getting house with id {pk}", exc_info=True)
          return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
    @swagger_auto_schema(
        operation_description="Retrieve room details for the tenant",
        operation_summary="Retrieve Room For tenant",
        method="get",
        tags=["room"],
        responses={
            200: openapi.Response(
                description="Retrieve a room",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'property_id': openapi.Schema(type=openapi.TYPE_STRING),
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
                        'agent': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            roperties={
                                'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'middle_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                                'gender': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'avatar': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                        'room_category': openapi.Schema(type=openapi.TYPE_STRING),
                        'price': openapi.Schema(type=openapi.TYPE_STRING),
                        'rental_duration': openapi.Schema(type=openapi.TYPE_STRING),
                        'status': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'condition': openapi.Schema(type=openapi.TYPE_STRING),
                        'nearby_facilities': openapi.Schema(type=openapi.TYPE_STRING),
                        'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                        'security_features': openapi.Schema(type=openapi.TYPE_STRING),
                        'heating_cooling_system': openapi.Schema(type=openapi.TYPE_STRING),
                        'furnishing_status': openapi.Schema(type=openapi.TYPE_STRING),
                        'is_locked': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
            404: openapi.Response(
                description="Not found",
                schema=DetailResponseSerializer(many=False)
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal serevr error",
                schema=DetailResponseSerializer(many=False)
            ),
        },
    )
    @action(detail=True, methods=['get'])
    def room_detail(self, request: HttpRequest, pk: uuid.UUID=None):
        """Retrieve a specific room by ID."""
        try:
            
            room = Room.get_room_by_id(property_id=pk)
            
            if not room:
                return Response({"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResponseRoomSerializer(room, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
          logger.error(f"Un expected error occured while getting house with id {pk}", exc_info=True)
          return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
    @swagger_auto_schema(
        operation_description="List filtered rooms",
        operation_summary="Filtered Rooms",
        method="get",
        tags=["room"],
        responses={
            200: openapi.Response(
                description="A paginated list of rooms",
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
                                    'agent': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'user_id': openapi.Schema(type=openapi.TYPE_STRING),
                                            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                            'middle_name': openapi.Schema(type=openapi.TYPE_STRING),
                                            'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                                            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                                            'gender': openapi.Schema(type=openapi.TYPE_STRING),
                                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                                            'avatar': openapi.Schema(type=openapi.TYPE_STRING),
                                        }
                                    ),
                                    'room_category': openapi.Schema(type=openapi.TYPE_STRING),
                                    'price': openapi.Schema(type=openapi.TYPE_STRING),
                                    'rental_duration': openapi.Schema(type=openapi.TYPE_STRING),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'condition': openapi.Schema(type=openapi.TYPE_STRING),
                                    'nearby_facilities': openapi.Schema(type=openapi.TYPE_STRING),
                                    'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                                    'security_features': openapi.Schema(type=openapi.TYPE_STRING),
                                    'heating_cooling_system': openapi.Schema(type=openapi.TYPE_STRING),
                                    'furnishing_status': openapi.Schema(type=openapi.TYPE_STRING),
                                    'is_locked': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        )
                    }
                ),
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
                'room_category', openapi.IN_QUERY, 
                description="Category of the rooms", 
                type=openapi.TYPE_STRING,
                enum=[category.value for category in ROOM_CATEGORY]
            ),
            openapi.Parameter(
                'region', openapi.IN_QUERY, description="Region of the house location", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'district', openapi.IN_QUERY, description="District of the house location", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'minPrice', openapi.IN_QUERY, description="Minimum price of the house", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'maxPrice', openapi.IN_QUERY, description="Maximum price of the house", type=openapi.TYPE_STRING
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def room_filter(self, request: HttpRequest):
        room_category: str = request.GET.get('roomCategory')
        region: str = request.GET.get('region')
        district: str = request.GET.get('district')
        min_price: str = request.GET.get('minPrice')
        max_price: str = request.GET.get('maxPrice')

        try:
            min_price = Decimal(min_price) if min_price else None
            max_price = Decimal(max_price) if max_price else None
        except Exception as e:
            return Response({"detail": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            houses = Room.room_filter(room_category=room_category, region=region, district=district, min_price=min_price, max_price=max_price)
            
            
            paginator = PageNumberPagination()
            
            page = paginator.paginate_queryset(houses, request)
            if page is not None:
                serializer = ResponseRoomSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = ResponseRoomSerializer(houses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)