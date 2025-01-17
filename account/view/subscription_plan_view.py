from typing import cast
from django.forms import ValidationError
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from account.serializers import ResponseSubscriptionPlanSerailizer, RequestSubscriptionSerializer
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from payment.enums.payment_type import PaymentType
from payment.models import Payment
from shared.serializer.detail_response_serializer import DetailResponseSerializer
from subscription_plan.models import SubscriptionPlan
from user.models import User, Agent



logger = logging.getLogger(__name__)

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestSubscriptionSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_actions = {'subscribe'}

        if self.action in agent_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return SubscriptionPlan.objects.none()
    
    @swagger_auto_schema(
        operation_description="Retrieve subscriptions for the authenticated agent.",
        operation_summary="Retrieve subscription",
        method="get",
        tags=["account"],
        responses={
            200: openapi.Response(
                description="Plans retrieved successful",
                schema=ResponseSubscriptionPlanSerailizer(many=True)
            ), 
            404: openapi.Response(
                description="bad request",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            )
        },
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
        
    @swagger_auto_schema(
        operation_description="New subscription payment plan for the authenticated agent.",
        operation_summary="Subscription",
        method="post",
        tags=["account"],
        request_body=RequestSubscriptionSerializer,
        responses={
            201: openapi.Response(
                description="Subscription saved successfuk, pending for payment complition",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Frorbidden to perform the task due to unknown agent",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Plan not found",
                schema=DetailResponseSerializer(many=False)
            )
        },
    )
    @action(detail=False, methods=['post'])
    def subscribe(self, request: HttpRequest):
        request_serializer = RequestSubscriptionSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        user = cast(User, request.user)
        
        
        try:
            agent = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
            plan = SubscriptionPlan.get_plan_by_id(subscription_plan_id=validated_data.get("plan_id"))
            
            if agent is None:
                return Response(data={"detail": "You are forbidden to view this information"}, status=status.HTTP_404_NOT_FOUND)
            
            if plan is None:
                return Response(data={"detail": "Subscription plan not found"}, status=status.HTTP_404_NOT_FOUND)
            
            payment = Payment.create(
                phone_number=validated_data.get("phone_number"), 
                payment_type=PaymentType.ACCOUNT, 
                amount=plan.price, 
                agent=agent, 
                plan=plan
            )
            
            return Response(data={"detail": f"Successfully subscribed to {plan.name}, please finish your payment to activate account"}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)