import json
from typing import cast
from django.forms import ValidationError
from django.http import HttpRequest
from requests import HTTPError, Timeout
import requests
from rest_framework import viewsets, permissions, status
from account.serializers import ResponseSubscriptionPlanSerailizer, RequestSubscriptionSerializer
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from igs_backend import settings
from payment.enums.payment_type import PaymentType
from payment.models import Payment
from shared.serializer.detail_response_serializer import DetailResponseSerializer
from subscription_plan.models import SubscriptionPlan
from user.models import User, Agent
from utils.http_client import PaymentHttpClient
from django.db import transaction



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
    @transaction.atomic(savepoint=False)
    def subscribe(self, request: HttpRequest):
        request_serializer = RequestSubscriptionSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        user = cast(User, request.user)

        try:
            with transaction.atomic(): 
                agent = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
                plan = SubscriptionPlan.get_plan_by_id(subscription_plan_id=validated_data.get("plan_id"))

                if not agent:
                    return Response(data={"detail": "You are forbidden to view this information"}, status=status.HTTP_404_NOT_FOUND)

                if not plan:
                    return Response(data={"detail": "Subscription plan not found"}, status=status.HTTP_404_NOT_FOUND)

                payment = Payment.create(
                    phone_number=validated_data.get("phone_number"),
                    payment_type=PaymentType.ACCOUNT,
                    amount=plan.price,
                    agent=agent,
                    plan=plan
                )

                phone_number = payment.phone_number
                if phone_number.startswith('+255'):
                    phone_number = '0' + phone_number[4:]

                order_data = {
                    'buyer_email': payment.agent.email,
                    'buyer_name': f"{payment.agent.first_name} {payment.agent.middle_name} {payment.agent.last_name}",
                    'buyer_phone': phone_number,
                    'amount': int(payment.amount),
                    'account_id': settings.ACCOUNT_ID,
                    'webhook_url': f"{settings.APP_BASE}{settings.WEB_HOOK_URL}",
                    'metadata': json.dumps({
                        'payment_id': str(payment.payment_id),
                    }),
                    'api_key': settings.ZENOPAY_API_KEY,
                    'secret_key': settings.ZENOPAY_SECRET_KEY,
                }

                client = PaymentHttpClient(base_url=settings.ZENOPAY_BASE)
                response = client.make_payment(data=order_data)

                if response is None:
                    return Response({"detail": "Payment gateway error, please try again later"}, status=status.HTTP_502_BAD_GATEWAY)

                logger.info(f"Plan subscription for {payment.agent} with payload: {json.dumps(order_data)} and response: {response.text}")

                if response.status_code == 200:
                    response_data = response.json()
                    response_status: str = response_data.get("status")

                    if response_status.lower() == "error":
                        payment.delete()
                        return Response(data={"detail": response_data.get("message")}, status=status.HTTP_400_BAD_REQUEST)

                    payment.update_order_and_message(order_id=response_data.get("order_id"), message=response_data.get("message"))
                    return Response(data={"detail": f"Successfully subscribed to {plan.name}, please complete your payment to activate your account."}, status=status.HTTP_200_OK)

                payment.delete()
                return Response(data={"detail": "Unexpected error with payment gateway"}, status=status.HTTP_502_BAD_GATEWAY)

        except requests.Timeout as e:
            logger.error(f"Request timeout occurred: {e}", exc_info=True)
            payment.delete()
            return Response({"detail": "Payment request timed out. Please try again later."}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except requests.RequestException as e:
            logger.error(f"HTTP error occurred: {e}", exc_info=True)
            payment.delete()
            return Response({"detail": "Payment gateway error occurred. Please try again later."}, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            payment.delete()
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)