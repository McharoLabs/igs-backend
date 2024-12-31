from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from user.models import LandLord
from user.serializers import (
    RequestLandLordRegistrationSerializer,
    ResponseLandLordRegistrationSerializer
)
import logging

logger = logging.getLogger(__name__)

class LandLordViewSet(viewsets.ViewSet):
    """
    ViewSet for handling landlord registration.
    """
    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'register_landlord':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        This method returns the appropriate serializer for the action.
        """
        return RequestLandLordRegistrationSerializer

    @swagger_auto_schema(
        operation_description="Register a new landlord in the system.",
        operation_summary="Landlord Registration",
        tags=["Registration"],
        request_body=RequestLandLordRegistrationSerializer,
        responses={
            201: ResponseLandLordRegistrationSerializer(many=False),
            400: "Invalid input data"
        },
    )
    @action(detail=False, methods=['post'], url_path='register')
    def register_landlord(self, request: HttpRequest):
        """
        Registers a new landlord based on provided data.
        """
        request_serializer = self.get_serializer_class()(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        try:
            landlord = LandLord.objects.create(
                first_name=validated_data.get("first_name"),
                middle_name=validated_data.get("middle_name"),
                last_name=validated_data.get("last_name"),
                phone_number=validated_data.get("phone_number"),
                gender=validated_data.get("gender"),
                email=validated_data.get("email"),
                password=validated_data.get("password"),
                avatar=validated_data.get("avatar", None)
            )
            response_serializer = ResponseLandLordRegistrationSerializer(landlord)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error during landlord registration: {str(e)}")
            return Response(data={"detail": "Landlord registration failed."}, status=status.HTTP_400_BAD_REQUEST)
