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
from house.enums.category import CATEGORY
from house.models import House
from house.serializers import RequestHouseSerializer, ResponseHouseSerializer, ResponseHouseDetailSerializer, ResponseMyHouseSerializer
from location.models import District
from location.models import Location
from property.models import Property
from property_images.models import PropertyImage
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.core.exceptions import PermissionDenied

from user.models import Agent
from user.models import User

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


logger = logging.getLogger(__name__)

@method_decorator(never_cache, name='dispatch')
class HouseViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestHouseSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_house' or self.action == 'list_houses' or self.action == 'retrieve_house':
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return House.objects.none()

    @swagger_auto_schema(
        operation_description="Add a new house by providing the necessary details such as agent, location, price, etc.",
        operation_summary="Create New House",
        method="post",
        tags=["house"],
        request_body=RequestHouseSerializer,
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
    def add_house(self, request: HttpRequest): 
        user = cast(User, request.user)      
        request_serializer = RequestHouseSerializer(data=request.data)
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

                response = House.save_house(
                    location=location, 
                    description=validated_data.get("description"), 
                    price=validated_data.get("price"), 
                    condition=validated_data.get("condition"), 
                    nearby_facilities=validated_data.get("nearby_facilities"),
                    category=validated_data.get("category"),
                    utilities=validated_data.get("utilities"),
                    security_features=validated_data.get("security_features"),
                    heating_cooling_system=validated_data.get("heating_cooling_system"),
                    furnishing_status=validated_data.get("furnishing_status"),
                    total_bath_room=validated_data.get("total_bath_room"),
                    total_bed_room=validated_data.get("total_bed_room"),
                    total_dining_room=validated_data.get("total_dining_room"),
                    agent=agent
                )
                
                property = Property.get_property_by_id(property_id=response.property_id)
                
                PropertyImage.save(property=property, images=validated_data.get("images"))

                response_serializer = DetailResponseSerializer({"detail": "House uploaded successful"})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Retrieve a house by its ID",
        operation_summary="Retrieve House",
        method="get",
        tags=["house"],
        responses={
            200: ResponseHouseDetailSerializer(many=False), 
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
    def retrieve_house(self, request: HttpRequest, pk: uuid.UUID=None):
        """Retrieve a specific house by ID."""
        try:
            user = cast(User, request.user)
            agent: Agent = None

            if hasattr(user, 'agent'):
                agent = cast(Agent, user)
            else:
                return Response(data={"detail": "you are not authorized to view this resource"}, status=status.HTTP_401_UNAUTHORIZED)
            
            house = House.get_agent_house(agent=agent, property_id=pk)
            
            if not house:
                return Response({"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResponseHouseDetailSerializer(house, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
          logger.error(f"Un expected error occured while getting house with id {pk}", exc_info=True)
          return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
    @swagger_auto_schema(
        operation_description="Retrieve house details for the tenant",
        operation_summary="Retrieve House Detail For Tenant",
        method="get",
        tags=["house"],
        responses={
            200: ResponseHouseDetailSerializer(many=False), 
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
    def house_detail(self, request: HttpRequest, pk: uuid.UUID=None):
        """Retrieve a specific house by ID."""
        try:
            
            house = House.get_house_by_id(property_id=pk)
            
            if not house:
                return Response({"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResponseHouseDetailSerializer(house, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
          logger.error(f"Un expected error occured while getting house with id {pk}", exc_info=True)
          return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="List all houses",
        operation_summary="List Houses",
        method="get",
        tags=["house"],
        responses={
            200: openapi.Response(
                description="A paginated list of houses",
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
                                    'category': openapi.Schema(type=openapi.TYPE_STRING),
                                    'price': openapi.Schema(type=openapi.TYPE_STRING),
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
    def list_houses(self, request: HttpRequest):
        user = cast(User, request.user)
        
        try:
            agent = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
            
            if agent is None:
                return Response(data={"detail": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
            
            houses = House.get_agent_houses(agent=agent)
            
            paginator = PageNumberPagination()
            page = paginator.paginate_queryset(houses, request)

            if page is not None:
                serializer = ResponseMyHouseSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = ResponseMyHouseSerializer(houses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except PermissionDenied as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
    @swagger_auto_schema(
        operation_description="List filtered houses",
        operation_summary="Filtered Houses",
        method="get",
        tags=["house"],
        responses={
            200: openapi.Response(
                description="A paginated list of houses",
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
                'category', openapi.IN_QUERY, 
                description="Category of the house (e.g., Rental, Sale)", 
                type=openapi.TYPE_STRING,
                enum=[category.value for category in CATEGORY]
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
    def filter_houses(self, request: HttpRequest):
        category: str = request.GET.get('category')
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
            houses = House.house_filter(category=category, region=region, district=district, min_price=min_price, max_price=max_price)
            
            
            paginator = PageNumberPagination()
            
            page = paginator.paginate_queryset(houses, request)
            if page is not None:
                serializer = ResponseHouseSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = ResponseHouseSerializer(houses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)