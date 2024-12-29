from typing import cast
from django.forms import ValidationError
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from account.models import SubscriptionPlan
from account.serializers import ResponseSubscriptionPlanSerailizer, RequestSubscriptionSerializer
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import logging

from payment.enums.payment_type import PaymentType
from payment.models import Payment
from shared.serializer.detail_response_serializer import DetailResponseSerializer
from user.models import User, Agent, LandLord



logger = logging.getLogger(__name__)

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestSubscriptionSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_landlord_actions = {'subscribe'}

        if self.action in agent_landlord_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        else:
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
        
    @swagger_auto_schema(
        operation_description="New subscription payment plan for the authenticated agent or landlord.",
        operation_summary="Subscription",
        method="post",
        tags=["Account"],
        request_body=RequestSubscriptionSerializer,
        responses={
            200: DetailResponseSerializer(many=False),
            400: "Invalid input data"
        },
    )
    @action(detail=False, methods=['post'])
    def subscribe(self, request: HttpRequest):
        request_serializer = RequestSubscriptionSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        user = cast(User, request.user)
        
        agent = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
        landlord = LandLord.get_landlord_by_phone_number(phone_number=user.phone_number)
        plan = SubscriptionPlan.get_plan_by_id(subscription_plan_id=validated_data.get("plan_id"))
        
        if agent is None and landlord is None:
            return Response(data={"detail": "You are forbidden to view this information"}, status=status.HTTP_404_NOT_FOUND)
        
        if plan is None:
            return Response(data={"detail": "Subscription plan not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            payment = Payment.create_payment(
                phone_number=validated_data.get("phone_number"), 
                payment_type=PaymentType.ACCOUNT, 
                amount=plan.price, 
                agent=agent, 
                landlord=landlord, 
                plan=plan
            )
            
            return Response(data={"detail": "You have initiated payment, please finish your payment to activate account"}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)