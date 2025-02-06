from typing import cast
import uuid
from django.http import Http404, HttpRequest, HttpResponse
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from igs_backend import settings
from property.models import Property
from property.serializers import RequestPropertyStatusSerializer
from property_images.models import PropertyImage
from shared.seriaizers import DetailResponseSerializer
import logging
import os
import mimetypes

from user.models import Agent, User


logger = logging.getLogger(__name__)

class PropertyViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestPropertyStatusSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        agent_actions = {'mark_property_rented', 'mark_property_sold', 'mark_property_available'}

        if self.action in agent_actions:
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return Property.objects.none()
    
    @swagger_auto_schema(
        operation_description="Mark property rented for authorized agent",
        operation_summary="mark property rented",
        method="post",
        tags=["propertyStatus"],
        responses={
            200: openapi.Response(
                description="Successful marked rented",
                schema=DetailResponseSerializer(many=False)
            ), 
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Bad request",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            )
        },
    )
    @action(detail=True, methods=['post'])
    def mark_property_rented(self, request: HttpRequest, pk: uuid.UUID):
        user = cast(User, request.user)
        
        agent: Agent = None
        
        if hasattr(user, 'agent'):
            agent = cast(Agent, user)
        else:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:                
            Property.mark_property_rented(property_id=pk, agent=agent)
            
            
            return Response(data={"detail": f"Successful status changed to rented"}, status=status.HTTP_200_OK)
        except Http404 as e:
            logger.error(f"Error occured error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Mark property sold for authorized agent",
        operation_summary="mark property sold",
        method="post",
        tags=["propertyStatus"],
        responses={
            200: openapi.Response(
                description="Successful marked sold",
                schema=DetailResponseSerializer(many=False)
            ), 
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Bad request",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            )
        },
    )
    @action(detail=True, methods=['post'])
    def mark_property_sold(self, request: HttpRequest, pk: uuid.UUID):
        user = cast(User, request.user)
        
        agent: Agent = None
        
        if hasattr(user, 'agent'):
            agent = cast(Agent, user)
        else:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:                
            Property.mark_property_sold(property_id=pk, agent=agent)
            
            
            return Response(data={"detail": f"Successful status changed to sold"}, status=status.HTTP_200_OK)
        except Http404 as e:
            logger.error(f"Error occured error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    @swagger_auto_schema(
        operation_description="Mark property available for authorized agent",
        operation_summary="mark property available",
        method="post",
        tags=["propertyStatus"],
        responses={
            200: openapi.Response(
                description="Successful marked available",
                schema=DetailResponseSerializer(many=False)
            ), 
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
            400: openapi.Response(
                description="Bad request",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=DetailResponseSerializer(many=False)
            )
        },
    )
    @action(detail=True, methods=['post'])
    def mark_property_available(self, request: HttpRequest, pk: uuid.UUID):
        user = cast(User, request.user)
        
        agent: Agent = None
        print(user)
        
        if hasattr(user, 'agent'):
            agent = cast(Agent, user)
        else:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:                
            Property.mark_property_available(property_id=pk, agent=agent)
            
            
            return Response(data={"detail": f"Successful status changed to available"}, status=status.HTTP_200_OK)
        except Http404 as e:
            logger.error(f"Error occured error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)