from typing import cast
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from account.models import SubscriptionPlan
from house.models import House, Room
from payment.serializers import RequestBookingPaymentSerializer, RequestSubscriptionPaymentSerializer
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
import logging

from payment.enums.payment_type import PaymentType
from payment.models import Payment
from shared.serializer.detail_response_serializer import DetailResponseSerializer
from user.models import User, Agent


logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ModelViewSet):
    pass