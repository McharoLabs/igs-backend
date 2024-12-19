from rest_framework import generics, permissions, status
from rest_framework.response import Response
from authentication.serializers import SignOutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from shared.seriaizers import DetailResponseSerializer

class SignOutAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SignOutSerializer

    @swagger_auto_schema(
        operation_description="This logs out the user and blacklist the token",
        operation_summary="Log out",
        tags=["Authentication"],
        request_body=SignOutSerializer,
        responses={
            200: DetailResponseSerializer(many=False),
            400: "Invalid input data"
        },
    )
    def post(self, request):
        serializer = SignOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Blacklist the refresh token
            token = serializer.validated_data['refresh']
            RefreshToken(token).blacklist()
            response_serializer = DetailResponseSerializer({"detail": "You have signed out successful"})
            return Response(data=response_serializer.data, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)