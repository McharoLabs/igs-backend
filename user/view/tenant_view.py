from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from user.models import Tenant
from user.serializers import (
    RequestTenantRegistrationSerializer,
    ResponseTenantRegistrationSerializer
)
import logging

logger = logging.getLogger(__name__)

class TenantRegistrationView(generics.GenericAPIView):
    """
    View to handle the registration of tenants.
    """
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Register a new tenant in the system.",
        operation_summary="Tenant Registration",
        tags=["Tenant Registration"],
        request_body=RequestTenantRegistrationSerializer,
        responses={
            201: ResponseTenantRegistrationSerializer(many=False),
            400: "Invalid input data"
        },
    )
    def post(self, request, *args, **kwargs):
        request_serializer = RequestTenantRegistrationSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        try:
            Tenant.save_tenant(
                first_name=validated_data.get("first_name"),
                middle_name=validated_data.get("middle_name"), 
                last_name=validated_data.get("last_name"), 
                phone_number=validated_data.get("phone_number"), 
                gender=validated_data.get("gender"), 
                username=validated_data.get("username"), 
                email=validated_data.get("email"), 
                password=validated_data.get("password"), 
                avatar=validated_data.get("avatar", None)
            )
            response_serializer = ResponseTenantRegistrationSerializer({"detail": "Tenant registration successful."})
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)