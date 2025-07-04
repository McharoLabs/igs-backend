from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from shared.serializer.detail_response_serializer import DetailResponseSerializer
from user.models import Agent
from user.serializers import RequestAgentRegistrationSerializer
import logging
from django.core.exceptions import ValidationError
from django.db import IntegrityError


logger = logging.getLogger(__name__)

class AgentViewSet(viewsets.ViewSet):
    """
    ViewSet for handling agent registration.
    """
    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'register_agent':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        This method returns the appropriate serializer for the action.
        """
        return RequestAgentRegistrationSerializer
    
    @swagger_auto_schema(
        operation_description="Register a new agent in the system.",
        operation_summary="Agent Registration",
        tags=["Registration"],
        request_body=RequestAgentRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="Agent registration succesful",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Bad request, invalid data provided",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            ),
        },
    )
    @action(detail=False, methods=['post'], url_path='register')
    def register_agent(self, request: HttpRequest):
        """
        Registers a new agent based on provided data.
        """
        request_serializer = RequestAgentRegistrationSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        try:
            
            Agent.save_agent(
                first_name=validated_data.get("first_name"),
                middle_name=validated_data.get("middle_name"),
                last_name=validated_data.get("last_name"),
                phone_number=validated_data.get("phone_number"),
                gender=validated_data.get("gender"),
                email=validated_data.get("email"),
                password=validated_data.get("password"),
                avatar=validated_data.get("avatar")
            )
            
            return Response(data={"detail": "Hongera, umefanikiwa kujisajili. Ndani ya dakika moja utapokea ujumbe wa meseji, tafadhali soma kwa umakini na baada ya hapo unaweza ingia kwenye mfumo na kutanganza nasi"}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"Validation during agent registration: {e}", exc_info=True)
            return Response(
                data={"detail": e.messages[0] if hasattr(e, "messages") else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        except IntegrityError as e:
            logger.error(f"Database IntegrityError during agent registration: {e}", exc_info=True)
            return Response(
                data={"detail": "Namba ya simu au barua pepe tayari imesajiliwa. Tafadhali tumia nyingine."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            logger.error(f"Error during agent registration: {str(e)}")
            return Response(data={"detail": {str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)