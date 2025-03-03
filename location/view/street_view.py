import uuid
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from location.models import Ward, Street
from location.serializers import RequestStreetSerializer
import logging
from drf_yasg import openapi

logger = logging.getLogger(__name__)


class StreetViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestStreetSerializer
    
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
        operation_description="Retrieve a Street by its ID",
        operation_summary="Retrieve Street",
        method="get",
        tags=["Location"],
        responses={200: RequestStreetSerializer(many=False), 404: "Street not found"},
    )
    @action(detail=True, methods=['get'])
    def retrieve_Street(self, request, pk=None):
        """Retrieve a specific Ward by ID."""
        street = Street.get_street_by_id(street_id=pk)
        if not street:
            return Response({"detail": "street not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RequestStreetSerializer(Street, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Retrieve Streets by Ward ID",
        operation_summary="Retrieve Streets by Ward ID",
        method="get",
        tags=["Location"],
        responses={
            200: RequestStreetSerializer(many=True),
            400: "Street is required",
            404: "Street not found"
        },
        manual_parameters=[
            openapi.Parameter(
                'ward_id',
                openapi.IN_PATH,
                description="The UUID of the Ward to retrieve Streets for",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='(?P<ward_id>[^/]+)/retrieve_ward_streets')
    def retrieve_ward_streets(self, request, ward_id: uuid.UUID):
        """Retrieve Streets for a specific region by region ID."""
        try:
            ward = Ward.get_ward_by_id(ward_id=ward_id)

            if not ward:
                return Response({"detail": "street not found"}, status=status.HTTP_404_NOT_FOUND)

            wards = Street.get_streets_by_Ward(ward=ward)

            serializer = RequestStreetSerializer(wards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any errors during the request
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)