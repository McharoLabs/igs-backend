from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from user.models import Agent
from user.serializers import (
    RequestAgentRegistrationSerializer,
    ResponseAgentRegistrationSerializer
)
import logging

logger = logging.getLogger(__name__)

class AgentRegistrationView(generics.GenericAPIView):
    """
    View to handle the registration of agents.
    """
    permission_classes = (permissions.AllowAny,)

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
    def post(self, request, *args, **kwargs):
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
                username=validated_data.get("username"), 
                email=validated_data.get("email"), 
                password=validated_data.get("password"), 
                avatar=validated_data.get("avatar", None)
            )
            response_serializer = ResponseAgentRegistrationSerializer({"detail": "Agent registration successful."})
            return Response(data=response_serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(data={"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)