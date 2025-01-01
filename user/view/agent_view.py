from django.http import HttpRequest
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from user.models import Agent
from user.serializers import (
    RequestAgentRegistrationSerializer,
    ResponseAgentRegistrationSerializer
)
import logging
from django.core.exceptions import ValidationError

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
            201: ResponseAgentRegistrationSerializer(many=False),
            400: "Invalid input data"
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
            
            agent = Agent.save_agent(
                first_name=validated_data.get("first_name"),
                middle_name=validated_data.get("middle_name"),
                last_name=validated_data.get("last_name"),
                phone_number=validated_data.get("phone_number"),
                gender=validated_data.get("gender"),
                email=validated_data.get("email"),
                password=validated_data.get("password"),
                avatar=validated_data.get("avatar")
            )
            response_serializer = ResponseAgentRegistrationSerializer(agent)
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.error(f"Error during agent registration: {str(e)}")
            return Response(data={"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error during agent registration: {str(e)}")
            return Response(data={"detail": "Agent registration failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)