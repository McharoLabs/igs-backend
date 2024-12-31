from rest_framework import authentication, generics, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.auth import TokenAuthentication
from authentication.serializers import SignInSerializer, TokenResponseSerializer
from drf_yasg.utils import swagger_auto_schema


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
        user = serializer.validated_data
        token = RefreshToken.for_user(user)
        data = {
            "tokens": {
                "refresh": str(token), 
                "access": str(token.access_token),
            }
        }
        
        response_serializer = TokenResponseSerializer(data)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK) 