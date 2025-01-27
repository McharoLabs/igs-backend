import json
from typing import cast
import uuid
from django.http import HttpRequest
import requests
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from booking.models import Booking
from booking.serializers import ResponseBookingSerailizer
from booking.serializers import  RequestBookingSerializer
from igs_backend import settings
from payment.enums.payment_type import PaymentType
from payment.models import Payment
from property.models import Property
from shared.seriaizers import DetailResponseSerializer
from rest_framework.pagination import PageNumberPagination
import logging

from user.model.user import User
from utils.http_client import HttpClient




logger = logging.getLogger(__name__)

class BookingViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestBookingSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_actions = {'booked_rooms', 'agent_booked_properties', 'agent_booked_property'}

        if self.action in agent_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return Booking.objects.none()
    
    
    @swagger_auto_schema(
        operation_description="Retrieve agent booked properties for the authorized agent",
        operation_summary="Retrieve booked properties for an agent",
        method="get",
        tags=["booking"],
        responses={
            200: openapi.Response(
                description="Agent's booked properties",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'booking_id': openapi.Schema(type=openapi.TYPE_STRING),
                        'property': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'property_id': openapi.Schema(type=openapi.TYPE_STRING),
                                'category': openapi.Schema(type=openapi.TYPE_STRING),
                                'price': openapi.Schema(type=openapi.TYPE_STRING),
                                'description': openapi.Schema(type=openapi.TYPE_STRING),
                                'condition': openapi.Schema(type=openapi.TYPE_STRING),
                                'nearby_facilities': openapi.Schema(type=openapi.TYPE_STRING),
                                'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                                'security_features': openapi.Schema(type=openapi.TYPE_STRING),
                                'furnishing_status': openapi.Schema(type=openapi.TYPE_STRING),
                                'location': openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'location_id': openapi.Schema(type=openapi.TYPE_STRING),  # UUID
                                        'region': openapi.Schema(type=openapi.TYPE_STRING),
                                        'district': openapi.Schema(type=openapi.TYPE_STRING),
                                        'ward': openapi.Schema(type=openapi.TYPE_STRING),
                                        'latitude': openapi.Schema(type=openapi.TYPE_STRING),
                                        'longitude': openapi.Schema(type=openapi.TYPE_STRING),
                                    }
                                ),
                                'images': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_STRING),
                                ),
                            }
                        ),
                        'customer_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'customer_email': openapi.Schema(type=openapi.TYPE_STRING),
                        'customer_phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                        'has_owner_read': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
            ),
            404: openapi.Response(
                description="Booking not found",
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
    @action(detail=True, methods=['get'])
    def agent_booked_property(self, request: HttpRequest, pk: uuid.UUID):
        user = cast(User, request.user)

        try:
            booked_property: Booking | None = Booking.get_booked_property(booking_id=pk, agent=user)
            
            if booked_property is None:
                return Response(data={"detail": "No booking found"}, status=status.HTTP_404_NOT_FOUND)
            
            response_serializer = ResponseBookingSerailizer(booked_property, many=False)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occurred during fetching agent booked properties: {e}", exc_info=True)
            return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_description="Retrieve agent booked properties, authorized agent",
        operation_summary="Retrieve authorized agent booked properties",
        method="get",
        tags=["booking"],
        responses={
            200: openapi.Response(
                description="A list of agent's booked properties",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'next': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'previous': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                        'results': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'booking_id': openapi.Schema(type=openapi.TYPE_STRING),  # UUID of the booking
                                    'property': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'property_id': openapi.Schema(type=openapi.TYPE_STRING),
                                            'category': openapi.Schema(type=openapi.TYPE_STRING),
                                            'price': openapi.Schema(type=openapi.TYPE_STRING),
                                            'description': openapi.Schema(type=openapi.TYPE_STRING),
                                            'condition': openapi.Schema(type=openapi.TYPE_STRING),
                                            'nearby_facilities': openapi.Schema(type=openapi.TYPE_STRING),
                                            'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                                            'security_features': openapi.Schema(type=openapi.TYPE_STRING),
                                            'furnishing_status': openapi.Schema(type=openapi.TYPE_STRING),
                                            'location': openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'location_id': openapi.Schema(type=openapi.TYPE_STRING),  # UUID
                                                    'region': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'district': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'ward': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'latitude': openapi.Schema(type=openapi.TYPE_STRING),
                                                    'longitude': openapi.Schema(type=openapi.TYPE_STRING),
                                                }
                                            ),
                                            'images': openapi.Schema(
                                                type=openapi.TYPE_ARRAY,
                                                items=openapi.Schema(type=openapi.TYPE_STRING),
                                            ),
                                        }
                                    ),
                                    'customer_name': openapi.Schema(type=openapi.TYPE_STRING),
                                    'customer_email': openapi.Schema(type=openapi.TYPE_STRING),
                                    'customer_phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                                    'has_owner_read': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                                }
                            )
                        )
                    }
                ),
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            ),
        }
    )
    @action(detail=False, methods=['get'])
    def agent_booked_properties(self, request: HttpRequest):
        user = cast(User, request.user)
        
        try:
            booked_properties = Booking.get_booked_properties(agent=user)
            
            paginator = PageNumberPagination()
            page = paginator.paginate_queryset(booked_properties, request)

            if page is not None:
                response_serializer = ResponseBookingSerailizer(page, many=True)
                return paginator.get_paginated_response(response_serializer.data)
            
            response_serializer = ResponseBookingSerailizer(booked_properties, many=True)
            return Response(data=response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"An error occured during fetching agent booked properties: {e}", exc_info=True)
            return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    @swagger_auto_schema(
        operation_description="Make booking by providong necessary information such as property ID and tenant phoe number",
        operation_summary="Tenant booking",
        method="post",
        tags=["booking"],
        request_body=RequestBookingSerializer,
        responses={
            200: openapi.Response(
                description="Success",
                schema=DetailResponseSerializer(many=False),
            ),
            403: openapi.Response(
                description="Bad request, Property not available for booking",
                schema=DetailResponseSerializer(many=False)
            ),
            404: openapi.Response(
                description="Not found",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Bad request",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            ),
        },
    )
    @action(detail=False, methods=['post'])
    def make_booking(self, request: HttpRequest):
        request_serializer = RequestBookingSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        property = Property.get_property_for_booking(property_id=validated_data.get("property_id"))
        
        if not property:
            return Response(data={"detail": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

        if not property.available():
            return Response(data={"detail": "Property not available for booking"}, status=status.HTTP_403_FORBIDDEN)

        try:
            payment = Payment.create(
                phone_number=validated_data.get("phone_number"),
                payment_type=PaymentType.BOOKING,
                amount=settings.BOOKING_FEE,
                property=property,
            )
            
            phone_number = payment.phone_number
            if phone_number.startswith('+255'):
                phone_number = '0' + phone_number[4:]
            
            order_data = {
                    'buyer_email': validated_data.get('customer_email'),
                    'buyer_name': validated_data.get('customer_name'),
                    'buyer_phone': phone_number,
                    'amount': float(payment.amount),
                    'account_id': settings.ACCOUNT_ID,
                    'webhook_url': f"{settings.APP_BASE}{settings.WEB_HOOK_URL}",
                    'metadata': json.dumps({
                        'payment_id': str(payment.payment_id),
                        'customer_name': validated_data.get('customer_name'),
                        'customer_email': validated_data.get('customer_email'), 
                    }),
                    'api_key': settings.ZENOPAY_API_KEY,
                    'secret_key': settings.ZENOPAY_SECRET_KEY,
                }

            client = HttpClient(base_url=settings.ZENOPAY_BASE)
            response = client.make_payment(data=order_data)

            if response is None:
                return Response({"detail": "Payment gateway error, please try again later"}, status=status.HTTP_502_BAD_GATEWAY)

            logger.info(f"Booking payment for property {property} with payload: {json.dumps(order_data)} and response: {response.text}")

            if response.status_code == 200:
                response_data = response.json()
                response_status = response_data.get("status")

                if response_status.lower() == "error":
                    payment.delete() 
                    return Response(data={"detail": response_data.get("message")}, status=status.HTTP_400_BAD_REQUEST)

                payment.update_order_and_message(order_id=response_data.get("order_id"), message=response_data.get("message"))
                return Response(data={"detail": "Booking initiated. Please complete your payment to confirm your booking."}, status=status.HTTP_200_OK)

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