from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from location.models import Region
from location.serializers import *
from shared.seriaizers import DetailResponseSerializer
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

class RegionViewSet(viewsets.ViewSet):    
    def get_serializer_class(self):
        return RequestRegionSerializer
    
    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_region':
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Region.objects.none()

    @swagger_auto_schema(
        operation_description="Add a new region by providing a new region name",
        operation_summary="Create New Region",
        method="post",
        tags=["Region"],
        request_body=RequestRegionSerializer,
        responses={200: DetailResponseSerializer(many=False), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['post'])
    def add_region(self, request):
        """Custom action to add a new region."""
        request_serializer = RequestRegionSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        if Region.is_region_by_name_exists(region_name=validated_data.get("region_name")):
            return Response(data={"detail": "Region already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            region_response = Region.add_region(region_name=validated_data.get("region_name"))
            response_serializer = DetailResponseSerializer({"detail": region_response})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            logger.error(f"Integrity error occurred: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}")
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Retrieve a region by its ID",
        operation_summary="Retrieve Region",
        method="get",
        tags=["Region"],
        responses={200: RequestRegionSerializer(many=False), 404: "Region not found"},
    )
    @action(detail=True, methods=['get'])
    def retrieve_region(self, request, pk=None):
        """Retrieve a specific region by ID."""
        region = Region.get_region_by_id(region_id=pk)
        if not region:
            return Response({"detail": "Region not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResponseRegionSerializer(region, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="List all regions",
        operation_summary="List Regions",
        method="get",
        tags=["Region"],
        responses={200: ResponseRegionSerializer(many=True)},
    )
    @action(detail=False, methods=['get'])
    def list_regions(self, request):
        """List all regions."""
        regions = Region.get_regions()
        serializer = ResponseRegionSerializer(regions, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
