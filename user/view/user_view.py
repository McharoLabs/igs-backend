import mimetypes
import os
from typing import cast
from django.http import  HttpRequest, HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from authentication.custom_permissions import *
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from igs_backend import settings
import logging

from user.models import User
from user.serializers import RequestAvatarSerializer


logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return RequestAvatarSerializer

    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'serve_avatar':
            permission_classes = [permissions.IsAuthenticated, IsAgentOrLandLord]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return None

    @swagger_auto_schema(
        operation_description="Get avator for the authenticated agent or landlord",
        operation_summary="Avator view",
        method="get",
        tags=["User"],
        responses={404: "No data found"},
    )
    @action(detail=False, methods=['get'])
    def serve_avatar(self, request: HttpRequest):
        try:
            user = cast(User, request.user)

            file_path = os.path.join(settings.MEDIA_ROOT, user.avatar.name)

            if not os.path.exists(file_path):
                return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

            mime_type, _ = mimetypes.guess_type(file_path)

            if mime_type is None:
                mime_type = 'application/octet-stream'

            with open(file_path, 'rb') as image_file:
                response = HttpResponse(image_file.read(), content_type=mime_type)
                return response

        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
