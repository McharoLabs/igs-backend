from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from account.models import SubscriptionPlan
from account.serializers import RequestSubscriptionPlanSerializer, ResponseSubscriptionPlanSerailizer
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import logging



logger = logging.getLogger(__name__)

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestSubscriptionPlanSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return SubscriptionPlan.objects.none()
    
    @swagger_auto_schema(
        operation_description="Retrieve subscriptions for the authenticated agent or landlord.",
        operation_summary="Retrieve subscription",
        method="get",
        tags=["Account"],
        responses={200: ResponseSubscriptionPlanSerailizer(many=True), 400: "Invalid input data"},
    )
    @action(detail=False, methods=['get'])
    def get_subscription(self, request: HttpRequest):

        try:
          response = SubscriptionPlan.get_all_plans()
          response_serializer = ResponseSubscriptionPlanSerailizer(response, many=True)
          return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)