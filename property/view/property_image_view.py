from typing import cast
from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import *
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from igs_backend import settings
from property.models import Property
from property.serializers import RequestPropertyImageSerializer
from property_images.models import PropertyImage
from shared.seriaizers import DetailResponseSerializer
import logging
import os
import mimetypes

from user.models import Agent, User


logger = logging.getLogger(__name__)

class PropertyImageViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestPropertyImageSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'upload_images':
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return PropertyImage.objects.none()
    
    @swagger_auto_schema(
        operation_description="Add property images by providing necessary details like house id and an array of images, etc.",
        operation_summary="Add property images",
        method="post",
        tags=["property"],
        request_body=RequestPropertyImageSerializer,
        responses={
            201: openapi.Response(
                description="Sucessful images added for the property",
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
    @action(detail=False, methods=['post'])
    def upload_images(self, request: HttpRequest):
        user = cast(User, request.user)
        request_serializer = RequestPropertyImageSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        agent: Agent = None
        
        if hasattr(user, 'agent'):
            agent = cast(Agent, user)
        else:
            return Response(data={"detail": "You are not authorized to perform this task"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:                
            property = Property.get_agent_property_by_id(agent=agent, property_id=validated_data.get("property_id"))
            
            if property is None:
                return Response(data={"detail": "Property not found not found"}, status=status.HTTP_404_NOT_FOUND)
            
            PropertyImage.save(property=property, images=validated_data.get("images"))
            
            return Response(data={"detail": f"You have successful uploded images"}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="View property image",
        operation_summary="View property image",
        method="get",
        tags=["property"],
        responses={
            200: "Image response", 
            400: "Invalid input data",
            404: "Image not found"
        },
        manual_parameters=[
            openapi.Parameter(
                'image_id',
                openapi.IN_PATH,
                description="The UUID of the image to retrieve",
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    @action(detail=False, methods=['get'], url_path='property-images/(?P<image_id>[^/]+)')
    def property_images(self, request, image_id):
        try:
            image = PropertyImage.get_image_by_id(image_id=image_id)

            image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))

            if not os.path.exists(image_path):
                return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                mime_type = 'application/octet-stream'

            with open(image_path, 'rb') as image_file:
                response = HttpResponse(image_file.read(), content_type=mime_type)
                return response

        except PropertyImage.DoesNotExist:
            return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



