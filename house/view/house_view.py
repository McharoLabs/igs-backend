from decimal import Decimal
from typing import cast
import uuid
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from house.enums.category import CATEGORY
from house.models import House
from house.serializers import RequestHouseSerializer, ResponseHouseSerializer, ResponseHouseDetailSerializer
from location.models import District
from location.models import Location
from shared.seriaizers import DetailResponseSerializer
import logging
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from django.core.exceptions import PermissionDenied

from user.models import User


logger = logging.getLogger(__name__)

class HouseViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestHouseSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_house' or self.action == 'list_houses':
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        elif self.action == 'retrieve_house':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return House.objects.none()

    @swagger_auto_schema(
        operation_description="Add a new house by providing the necessary details such as agent, landlord, location, price, etc.",
        operation_summary="Create New House",
        method="post",
        tags=["House"],
        request_body=RequestHouseSerializer,
        responses={200: DetailResponseSerializer(many=False), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['post'])
    @transaction.atomic(savepoint=False)
    def add_house(self, request):
        """Custom action to add a new house."""
        request_serializer = RequestHouseSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        district = District.get_district_by_id(district_id=validated_data.get("district_id"))
        if district is None:
            return Response(data={"detail": "District not found"}, status=status.HTTP_404_NOT_FOUND)

        landlord = LandLord.get_landlord_by_username(username=request.user)
        agent = Agent.get_agent_by_username(username=request.user)

        if landlord is None and agent is None:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            with transaction.atomic():
                location = Location.add_location(
                    region=district.region.name,
                    district=district.name,
                    ward=validated_data.get("ward"),
                    latitude=validated_data.get("latitude"),
                    longitude=validated_data.get("longitude")
                )

                data = {
                    "location": location,
                    "title": validated_data.get("title"),
                    "description": validated_data.get("description"),
                    "price": validated_data.get("price"),
                    "condition": validated_data.get("condition"),
                    "nearby_facilities": validated_data.get("nearby_facilities"),
                    "category": validated_data.get("category"),
                    "utilities": validated_data.get("utilities"),
                    "security_features": validated_data.get("security_features"),
                    "heating_cooling_system": validated_data.get("heating_cooling_system"),
                    "furnishing_status": validated_data.get("furnishing_status"),
                    "total_bed_room": validated_data.get("total_bed_room"),
                    "total_dining_room": validated_data.get("total_dining_room"),
                    "total_bath_room": validated_data.get("total_bath_room"),
                    "agent": agent,
                    "landlord": landlord
                }

                response_message = House.add_house(**data)

                response_serializer = DetailResponseSerializer({"detail": response_message})
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
        tags=["House"],
        responses={
            200: ResponseHouseDetailSerializer(many=False), 
            404: DetailResponseSerializer(many=False)
        },
    )
    @action(detail=True, methods=['get'])
    def retrieve_house(self, request: HttpRequest, pk: uuid.UUID=None):
        """Retrieve a specific house by ID."""
        house = House.get_house_by_id(house_id=pk)
        if not house:
            return Response({"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResponseHouseDetailSerializer(house)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="List all houses",
        operation_summary="List Houses",
        method="get",
        tags=["House"],
        responses={
            200: ResponseHouseSerializer(many=True), 
            401: DetailResponseSerializer(many=False)
        },
        manual_parameters=[
            openapi.Parameter(
                'house_id',
                openapi.IN_QUERY,
                description="House id for getting specific house for the agent or landlord",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def list_houses(self, request: HttpRequest):
        user = cast(User, request.user)
        house_id = request.GET.get('house_id')
        try:
            houses: House = None
            if hasattr(user, 'landlord'):
                houses = House.get_all_houses(landlord=user, house_id=house_id)
            elif hasattr(user, 'agent'):
                houses = House.get_all_houses(agent=user, house_id=house_id)
            else:
                houses = House.get_all_houses()
                
            serializer = ResponseHouseSerializer(houses, many=True)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
    @swagger_auto_schema(
        operation_description="List filtered houses",
        operation_summary="Filtered Houses",
        method="get",
        tags=["House"],
        responses={200: ResponseHouseSerializer(many=True)},
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
            houses = House.filter_houses(category=category, region=region, district=district, min_price=min_price, max_price=max_price)
            
            
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