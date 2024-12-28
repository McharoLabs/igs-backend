from decimal import Decimal
import json
from typing import cast
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from account.models import Account
from account.serializers import RequestSubscriptionPlanSerializer, ResponseAccountSerializer
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import logging

from shared.serializer.detail_response_serializer import DetailResponseSerializer
from user.models import User, Agent, LandLord


logger = logging.getLogger(__name__)

class AccountViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestSubscriptionPlanSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_landlord_actions = {'account'}

        if self.action in agent_landlord_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Account.objects.none()
    
    @swagger_auto_schema(
        operation_description="Retrieve active account information for the authenticated agent or landlord.",
        operation_summary="Retrieve active account information",
        method="get",
        tags=["Account"],
        responses={
            200: ResponseAccountSerializer(many=True),
            400: "Invalid input data"
        },
    )
    @action(detail=False, methods=['get'])
    def account(self, request: HttpRequest):
        user = cast(User, request.user)
        
        agent = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
        landlord = LandLord.get_landlord_by_phone_number(phone_number=user.phone_number)

        if agent is None and landlord is None:
            return Response(data={"detail": "You are forbidden to view this information"}, status=status.HTTP_404_NOT_FOUND)

        try:
            account = Account.get_account(agent=agent, landlord=landlord)
            response_serializer = ResponseAccountSerializer(account, many=False)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)