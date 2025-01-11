from decimal import Decimal
import json
from typing import cast
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from account.models import Account
from account.serializers import ResponseAccountSerializer, RequestSubscriptionSerializer
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import logging

from shared.serializer.detail_response_serializer import DetailResponseSerializer
from user.models import User, Agent
from drf_yasg import openapi


logger = logging.getLogger(__name__)

class AccountViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestSubscriptionSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_actions = {'account'}

        if self.action in agent_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Account.objects.none()
    
    @swagger_auto_schema(
        operation_description="Retrieve active account information for the authenticated agent.",
        operation_summary="Retrieve active account information",
        method="get",
        tags=["account"],
        responses={
            200: openapi.Response(
                description="Account retrieved successful",
                schema=ResponseAccountSerializer(many=False),
            ),
            400: openapi.Response(
                description="Account retrieved successful",
                schema=DetailResponseSerializer(many=False),
            ),
            404: openapi.Response(
                description="Forbidden to perform the task",
                schema=DetailResponseSerializer(many=False),
            ),
        },
    )
    @action(detail=False, methods=['get'])
    def account(self, request: HttpRequest):
        user = cast(User, request.user)

        try:
            agent: Agent | None = Agent.get_agent_by_phone_number(user.phone_number)
            
            if agent is None:
                return Response(data={"detail": "Agent not found"}, status=status.HTTP_404_NOT_FOUND)
            
            account = Account.get_account(agent=agent)
            response_serializer = ResponseAccountSerializer(account, many=False)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)