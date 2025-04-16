from decimal import Decimal
import logging
import mimetypes
import os
from typing import cast
import uuid
from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets, permissions, status
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.db import transaction, DatabaseError
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination

from igs_backend import settings
from land.enums.land_type import LAND_TYPE
from land.model.land import Land
from land.serializers import FilterLandSerializer, AddLandSerializer
from location.models import Location
from location.models import District
from property_images.models import LandImage
from shared.serializer.detail_response_serializer import DetailResponseSerializer
from user.model.agent import Agent
from user.models import User


logger = logging.getLogger(__name__)

@method_decorator(never_cache, name='dispatch')
class LandViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return AddLandSerializer
    
    def get_permissions(self):
        """
        Custom method to define permissions for each action.
        """
        if self.action == 'add_land' or self.action == 'land_list' or self.action == 'soft_delete_land':
            permission_classes = [permissions.IsAuthenticated, IsAgent]
        else:
            permission_classes = [permissions.AllowAny]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        return Land.objects.none()
    
    @swagger_auto_schema(
        operation_description="View Land image",
        operation_summary="View land image",
        method="get",
        tags=["Land"],
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
    @action(detail=False, methods=['get'], url_path='land-images/(?P<image_id>[^/]+)')
    def property_images(self, request, image_id):
        try:
            image = LandImage.get_image_by_id(image_id=image_id)

            image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))

            if not os.path.exists(image_path):
                return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

            mime_type, _ = mimetypes.guess_type(image_path)
            if not mime_type:
                mime_type = 'application/octet-stream'

            with open(image_path, 'rb') as image_file:
                response = HttpResponse(image_file.read(), content_type=mime_type)
                return response

        except LandImage.DoesNotExist:
            return Response({"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_summary="Soft delete land",
        operation_description="Soft delete land",
        method="delete",
        tags=["Land"],
        responses={
            200: openapi.Response(
                description="Deleted successful",
                schema=DetailResponseSerializer(many=False)
            ), 
            404: openapi.Response(
                description="Not found",
                schema=DetailResponseSerializer(many=False)
            ),
            401: openapi.Response(
                description="Unauthorized",
                schema=DetailResponseSerializer(many=False)
            ),
            403: openapi.Response(
                description="Forbidden",
                schema=DetailResponseSerializer(many=False)
            ),
            500: openapi.Response(
                description="Internal serevr error",
                schema=DetailResponseSerializer(many=False)
            ),
        },
    )
    @action(detail=True, methods=['delete'])
    def soft_delete_land(self, request: HttpRequest, pk:uuid.UUID=None):
        user = cast(User, request.user)
        
        try:
            agent: Agent | None = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
            
            if agent is None:
                return Response(data={"detail": "Huwezi fita hii ardhi kwasababu huna ruhusa inayohitajika"}, status=status.HTTP_403_FORBIDDEN)
            
            Land.soft_delete_land(land_id=pk, agent=agent)
            
            return Response(data={"detail": "Umefanikiwa kufuta ardhi"}, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            logger.error(f"Error occurred while deleting land: {e}",exc_info=True)
            return Response(data={"detail": e.messages}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Un expected error occured while deleting land {pk}", exc_info=True)
            return Response(data={"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="Add land by providing necessary details",
        operation_summary="Add land",
        method="post",
        tags=["Land"],
        request_body=AddLandSerializer,
        responses={
            201: openapi.Response(
                description="land added successful",
                schema=DetailResponseSerializer(many=False)
            ), 
            404: openapi.Response(
                description="District not found",
                schema=DetailResponseSerializer(many=False)
            ), 
            401: openapi.Response(
                description="Unauthorized, agent not recognized",
                schema=DetailResponseSerializer(many=False)
            ),
            403: openapi.Response(
                description="Forbidden",
                schema=DetailResponseSerializer(many=False)
            ),
            404: openapi.Response(
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
    @transaction.atomic(savepoint=False)
    def add_room(self, request: HttpRequest):
        user = cast(User, request.user)      
        request_serializer = AddLandSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        validated_data = request_serializer.validated_data
        
        try:
            district: District | None = District.get_district_by_id(district_id=validated_data.get("district_id"))
            
            if district is None:
                return Response(data={"detail": "District not found"}, status=status.HTTP_404_NOT_FOUND)

            agent: Agent | None = Agent.get_agent_by_phone_number(phone_number=user.phone_number)
            
            if agent is None:
                return Response(data={"detail": "Huruhusiwei kupakia mali, tafadhali ingia tena kwa namba yako ya simu na nywila"}, status=status.HTTP_403_FORBIDDEN)
            
            with transaction.atomic():
                location = Location.add_location(
                    region=district.region.name,
                    district=district.name,
                    ward=validated_data.get("ward"),
                    street=validated_data.get("street"),
                    latitude=validated_data.get("latitude"),
                    longitude=validated_data.get("longitude")
                )

                response = Land.save_land(
                    location=location,
                    description=validated_data.get("description"),
                    price=validated_data.get("price"),
                    rental_duration=validated_data.get("rental_duration"),
                    category=validated_data.get("category"),
                    land_size=validated_data.get("land_size"),
                    access_road_type=validated_data.get("access_road_type"),
                    zoning_type=validated_data.get("zoning_type"),
                    utilities=validated_data.get("utilities"),
                    is_serviced=validated_data.get("is_serviced"),
                    agent=agent,
                )
                
                LandImage.save(land=response, images=validated_data.get("images"))

                response_serializer = DetailResponseSerializer({"detail": "Umefanikiwa kupakia taarifa za ardhi"})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}", exc_info=True)
            error_message = getattr(e, 'message', None) or getattr(e, 'detail', None) or e
            return Response({"detail": error_message}, status=status.HTTP_400_BAD_REQUEST)

        except PermissionDenied as e:
            logger.warning(f"Permission error: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except DatabaseError as e:
            logger.critical(f"Database error: {e}", exc_info=True)
            return Response({"detail": "A database error occurred. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(
        operation_description="List filtered lands",
        operation_summary="Filtered Lands",
        method="get",
        tags=["Land"],
        responses={
            200: openapi.Response(
                description="A paginated list of lands",
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
                                    'land_id': openapi.Schema(type=openapi.TYPE_STRING),
                                    'category': openapi.Schema(type=openapi.TYPE_STRING),
                                    'land_size': openapi.Schema(type=openapi.TYPE_STRING),
                                    'price': openapi.Schema(type=openapi.TYPE_STRING),
                                    'rental_duration': openapi.Schema(type=openapi.TYPE_STRING),
                                    'access_road_type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'zoning_type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'utilities': openapi.Schema(type=openapi.TYPE_STRING),
                                    'is_serviced': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                                    'is_active_account': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                                    'is_deleted': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'listing_date': openapi.Schema(type=openapi.TYPE_STRING),
                                    'location': openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            'location_id': openapi.Schema(type=openapi.TYPE_STRING),
                                            'region': openapi.Schema(type=openapi.TYPE_STRING),
                                            'district': openapi.Schema(type=openapi.TYPE_STRING),
                                            'ward': openapi.Schema(type=openapi.TYPE_STRING),
                                            'street': openapi.Schema(type=openapi.TYPE_STRING),
                                            'latitude': openapi.Schema(type=openapi.TYPE_STRING),
                                            'longitude': openapi.Schema(type=openapi.TYPE_STRING),
                                        }
                                    ),
                                    'images': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(type=openapi.TYPE_STRING),
                                    ),
                                }
                            )
                        )
                    }
                ),
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
        manual_parameters=[
            openapi.Parameter(
                'category', openapi.IN_QUERY,
                description="Type of land",
                type=openapi.TYPE_STRING,
                enum=[category.value for category in LAND_TYPE]
            ),
            openapi.Parameter(
                'region', openapi.IN_QUERY,
                description="Region of the land location",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'district', openapi.IN_QUERY,
                description="District of the land location",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ward', openapi.IN_QUERY,
                description="Ward of the land location",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'street', openapi.IN_QUERY,
                description="Street of the land location",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'min_price', openapi.IN_QUERY,
                description="Minimum price of the land",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'max_price', openapi.IN_QUERY,
                description="Maximum price of the land",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def land_filter(self, request: HttpRequest):
        category: str = request.GET.get('category')
        region: str = request.GET.get('region')
        district: str = request.GET.get('district')
        min_price: str = request.GET.get('min_price')
        max_price: str = request.GET.get('max_price')
        street: str = request.GET.get('street')
        ward: str = request.GET.get('ward')

        try:
            min_price = Decimal(min_price) if min_price else None
            max_price = Decimal(max_price) if max_price else None
        except Exception as e:
            return Response({"detail": "Invalid price format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lands = Land.land_filter(
                category=category,
                region=region,
                district=district,
                ward=ward,
                street=street,
                min_price=min_price,
                max_price=max_price
            )

            paginator = PageNumberPagination()
            page = paginator.paginate_queryset(lands, request)
            if page is not None:
                serializer = FilterLandSerializer(page, many=True)
                return paginator.get_paginated_response(serializer.data)

            serializer = FilterLandSerializer(lands, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.error(f"Validation error occurred: {e}", exc_info=True)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred: {e}", exc_info=True)
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)