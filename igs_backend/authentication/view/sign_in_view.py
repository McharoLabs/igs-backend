from typing import cast
from rest_framework import authentication, generics, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.auth import TokenAuthentication
from authentication.serializers import SignInSerializer, TokenResponseSerializer
from drf_yasg.utils import swagger_auto_schema

from user.models import User


class SignInAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignInSerializer
    authentication_classes = [
            authentication.SessionAuthentication,
            TokenAuthentication,JWTAuthentication
        ]  
    
    @swagger_auto_schema(
        operation_description="User authentication",
        operation_summary="Authentication of the user",
        tags=["Authentication"],
        request_body=SignInSerializer,
        responses={
            200: TokenResponseSerializer(many=False),
            400: "Invalid input data"
        },
    )
    def post(self,request):
        serializer = SignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = cast(User, validated_data)
        token = RefreshToken.for_user(user)
        
        token.payload["is_agent"] = not user.is_superuser
        if not user.is_superuser:
            token.payload['test'] = user.last_name
            token.payload["full_name"] = f"{user.first_name} {user.last_name}"
            token.payload["email"] = user.email
        
        data = {
            "tokens": {
                "refresh": str(token), 
                "access": str(token.access_token),
            }
        }
        
        response_serializer = TokenResponseSerializer(data)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK) 