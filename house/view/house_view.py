from decimal import InvalidOperation
from typing import cast
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from house.models import House
from house.serializers import *
from location.models import District
from location.models import Location
from shared.seriaizers import DetailResponseSerializer
import logging
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


logger = logging.getLogger(__name__)

class HouseViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestHouseSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_house':
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        elif self.action == 'retrieve_house':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'list_houses':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return super().get_queryset()

    @swagger_auto_schema(
        operation_description="Add a new house by providing the necessary details such as agent, landlord, location, price, etc.",
        operation_summary="Create New House",
        method="post",
        tags=["House"],
        request_body=RequestHouseSerializer,
        responses={200: DetailResponseSerializer(many=False), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['post'])
    def add_house(self, request):
        """Custom action to add a new house."""
        request_serializer = RequestHouseSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        district = District.get_district_by_id(district_id=validated_data.get("district_id"))
        if district is None:
            return Response(data={"District not found"}, status=status.HTTP_404_NOT_FOUND)
        
        land_lord = LandLord.get_landlord_by_username(username=request.user)
        agent = Agent.get_agent_by_username(username=request.user)
        
        if land_lord is None and agent is None:
            return Response(data={"You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            location = cast(Location, Location.add_location(
                region=district.region.name, 
                district=district.name,
                ward=validated_data.get("ward"),
                latitude=validated_data.get("latitude"), 
                longitude=validated_data.get("longitude")
            ))
            
            response_message = House.add_house(
                agent=agent,
                landlord=land_lord,
                location=location,
                title=validated_data.get("title"),
                description=validated_data.get("description"),
                price_unit=validated_data.get("price_unit"),
                condition=validated_data.get("condition"),
                nearby_facilities=validated_data.get("nearby_facilities"),
                category=validated_data.get("category"),
                utilities=validated_data.get("utilities"),
                security_features=validated_data.get("security_features"),
                heating_cooling_system=validated_data.get("heating_cooling_system"),
                furnishing_status=validated_data.get("furnishing_status"),
                total_bed_room=validated_data.get("total_bed_room"),
                total_dining_room=validated_data.get("total_dining_room"),
                total_bath_room=validated_data.get("total_bath_room"),
                total_floor=validated_data.get("total_floor")
            )
            response_serializer = DetailResponseSerializer({"detail": response_message})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except InvalidOperation as e:
            logger.error(f"Invalid price unit: {e}", exc_info=True)
            return Response({"detail": "Price unit must be a valid decimal number."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Retrieve a house by its ID",
        operation_summary="Retrieve House",
        method="get",
        tags=["House"],
        responses={200: ResponseHouseSerializer(many=False), 404: "House not found"},
    )
    @action(detail=True, methods=['get'])
    def retrieve_house(self, request, pk=None):
        """Retrieve a specific house by ID."""
        house = House.get_house_by_id(house_id=pk)
        if not house:
            return Response({"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResponseHouseSerializer(house)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="List all houses",
        operation_summary="List Houses",
        method="get",
        tags=["House"],
        responses={200: ResponseHouseSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def list_houses(self, request):
        """List all houses."""
        houses = House.get_all_houses()
        serializer = ResponseHouseSerializer(houses, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="List filtered houses",
        operation_summary="Filtered Houses",
        method="get",
        tags=["House"],
        responses={200: ResponseHouseSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def filter_houses(self, request):
        filters = Q()
        
        category = request.query_params.get('category')
        region = request.query_params.get('region')
        district = request.query_params.get('district')
        min_price = request.query_params.get('minPrice')
        max_price = request.query_params.get('maxPrice')
        
        if category:
            filters &= Q(category=category)
        if region:
            filters &= Q(location__region__iexact=region)
        if district:
            filters &= Q(location__district__iexact=district)
        if min_price:
            filters &= Q(price_unit__gte=min_price)
        if max_price:
            filters &= Q(price_unit__lte=max_price)
            
        houses = House.objects.filter(filters).select_related('location').order_by('-house_id')
        
        paginator = PageNumberPagination()
        
        page = paginator.paginate_queryset(houses, request)
        if page is not None:
            serializer = ResponseHouseSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ResponseHouseSerializer(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
