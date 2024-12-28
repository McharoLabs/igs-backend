from typing import cast
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from account.models import SubscriptionPlan
from account.models import Account
from house.models import House, Room
from payment.serializers import RequestBookingPaymentSerializer, PaymentResponseSerializer, RequestSubscriptionPaymentSerializer
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

class PaymentViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestBookingPaymentSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_landlord_actions = {'new_plan'}

        if self.action in agent_landlord_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return None
    
    @swagger_auto_schema(
        operation_description="Booking for the tenant",
        operation_summary="Booking payment",
        method="post",
        tags=["Payment"],
        request_body=RequestBookingPaymentSerializer,
        responses={
            200: DetailResponseSerializer(many=True),
            400: "Invalid input data"
        },
    )
    @action(detail=False, methods=['post'])
    def book(self, request: HttpRequest):
        request_serializer = RequestBookingPaymentSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        house = House.get_house_by_id(house_id=validated_data.get("house_id"))
        room = Room.get_room(room_id=validated_data.get("room_id"))
        
        if house is None:
            return Response(data={"detail": "House not found"}, status=status.HTTP_404_NOT_FOUND)
        
        room = None
        if validated_data.get("room_id") is not None:
            room = Room.get_room(room_id=validated_data.get("room_id"))
            
            if room is None:
                return Response(data={"detail": "Room not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            payment = Payment.create_payment(
                phone_number=validated_data.get("phone_number"), 
                payment_type=PaymentType.BOOKING, 
                amount=validated_data.get("amount"), 
                house=house,
                room=room,
            )
            
            return Response(data={"detail": "You have initiated payment for booking, please finish your payment"}, status=status.HTTP_200_OK)
        except ValueError as e:
            logger.error(f"Value error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="New subscription payment plan for the authenticated agent or landlord.",
        operation_summary="Subscription Payment",
        method="post",
        tags=["Payment"],
        request_body=RequestSubscriptionPaymentSerializer,
        responses={
            200: DetailResponseSerializer(many=False),
            400: "Invalid input data"
        },
    )
    @action(detail=False, methods=['post'])
    def new_plan(self, request: HttpRequest):
        request_serializer = RequestSubscriptionPaymentSerializer(data=request.data)
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