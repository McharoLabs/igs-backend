import uuid
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from location.models import District, Region
from location.serializers import *
from shared.seriaizers import DetailResponseSerializer
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import logging
from drf_yasg import openapi

logger = logging.getLogger(__name__)

class DistrictViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestDistrictSerializer
    
    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_district':
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return District.objects.none()

    @swagger_auto_schema(
        operation_description="Add a new district by providing the district name and existing region id",
        operation_summary="Create New District",
        method="post",
        tags=["Location"],
        request_body=RequestDistrictSerializer,
        responses={200: DetailResponseSerializer(many=False), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['post'])
    def add_district(self, request):
        """Custom action to add a new district to an existing region."""
        request_serializer = RequestDistrictSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data

        if District.is_district_by_name_exists(district_name=validated_data.get("district_name")):
            return Response(data={"detail": "District already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if not Region.is_region_by_id_exists(region_id=validated_data.get("region_id")):
            return Response(data={"detail": "Region does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        region = Region.get_region_by_id(region_id=validated_data.get("region_id"))

        try:
            district_response = District.add_district(
                district_name=validated_data.get("district_name"),
                region=region
            )
            response_serializer = DetailResponseSerializer({"detail": district_response})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Integrity error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Retrieve a district by its ID",
        operation_summary="Retrieve District",
        method="get",
        tags=["Location"],
        responses={200: ResponseDistrictSerializer(many=False), 404: "District not found"},
    )
    @action(detail=True, methods=['get'])
    def retrieve_district(self, request, pk=None):
        """Retrieve a specific district by ID."""
        district = District.get_district_by_id(district_id=pk)
        if not district:
            return Response({"detail": "District not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResponseDistrictSerializer(district, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Retrieve districts by region ID",
        operation_summary="Retrieve districts by region ID",
        method="get",
        tags=["Location"],
        responses={
            200: ResponseDistrictSerializer(many=True),
            400: "Region is required",
            404: "Region not found"
        },
        manual_parameters=[
            openapi.Parameter(
                'region_id',
                openapi.IN_PATH,
                description="The UUID of the region to retrieve districts for",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='(?P<region_id>[^/]+)/retrieve_region_districts')
    def retrieve_region_districts(self, request, region_id: uuid.UUID):
        """Retrieve districts for a specific region by region ID."""
        try:
            region = Region.get_region_by_id(region_id=region_id)

            if not region:
                return Response({"detail": "Region not found"}, status=status.HTTP_404_NOT_FOUND)

            districts = District.get_districts_by_region(region=region)

            serializer = ResponseDistrictSerializer(districts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors during the request
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(
        operation_description="List all districts",
        operation_summary="List Districts",
        method="get",
        tags=["Location"],
        responses={200: ResponseDistrictSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def list_districts(self, request):
        """List all districts."""
        districts = District.get_all_districts()
        serializer = ResponseDistrictSerializer(districts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
# 612939fb-10d2-4cb8-86a8-449ec2b688ae
