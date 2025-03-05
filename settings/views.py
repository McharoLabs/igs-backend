from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from booking.serializers import RequestBookingSerializer
from settings.models import SiteSettings
import logging

from settings.serializers import SiteSettingsSerializer

logger = logging.getLogger(__name__)

class CompanyInformation(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        return SiteSettingsSerializer
    
    def get_queryset(self):
        return SiteSettings.objects.none()

    @swagger_auto_schema(
        operation_description="Retrieve company information",
        operation_summary="Retrieve company information",
        method="get",
        tags=["company_information"],
        responses={
            200: openapi.Response(
                description="Company information",
                schema=SiteSettingsSerializer,
            ),
            404: openapi.Response(
                description="No company information found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
        },
    )
    @action(detail=False, methods=['get'])
    def get_information(self, request):
        try:
            siteSettings: SiteSettings | None = SiteSettings.company_settings()

            if siteSettings is None:
                return Response(data={"detail": "No company information"}, status=status.HTTP_404_NOT_FOUND)

            response_serializer = SiteSettingsSerializer(siteSettings, many=False)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred during fetching company information: {e}", exc_info=True)
            return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
