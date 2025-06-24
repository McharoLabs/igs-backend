import uuid
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from location.models import District, Ward
from location.serializers import RequestWardSerializer
import logging
from drf_yasg import openapi

logger = logging.getLogger(__name__)


class WardViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestWardSerializer
    
    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_ward':
            permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return None
    
    @swagger_auto_schema(
        operation_description="Retrieve a ward by its ID",
        operation_summary="Retrieve Ward by ID",
        method="get",
        tags=["Location"],
        responses={200: RequestWardSerializer(many=False), 404: "Ward not found"},
    )
    @action(detail=True, methods=['get'])
    def retrieve_ward(self, request, pk=None):
        """Retrieve a specific district by ID."""
        ward = Ward.get_ward_by_id(ward_id=pk)
        if not ward:
            return Response({"detail": "Ward not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RequestWardSerializer(ward, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Retrieve wards by district ID",
        operation_summary="Retrieve wards by district ID",
        method="get",
        tags=["Location"],
        responses={
            200: RequestWardSerializer(many=True),
            400: "ward is required",
            404: "ward not found"
        },
        manual_parameters=[
            openapi.Parameter(
                'district_id',
                openapi.IN_PATH,
                description="The UUID of the district to retrieve wards for",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='(?P<district_id>[^/]+)/retrieve_district_wards')
    def retrieve_district_wards(self, request, district_id: uuid.UUID):
        """Retrieve wards for a specific region by region ID."""
        try:
            district = District.get_district_by_id(district_id=district_id)

            if not district:
                return Response({"detail": "ward not found"}, status=status.HTTP_404_NOT_FOUND)

            districts = Ward.get_wards_by_district(district=district)

            serializer = RequestWardSerializer(districts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors during the request
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)