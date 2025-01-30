from rest_framework import permissions, status, viewsets
from authentication.custom_permissions import IsAgent
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from message.models import MessageQueue
from message.serializers import MessageSerializer
from shared.seriaizers import DetailResponseSerializer
import logging

from utils.http_client import MessageHttpClient




logger = logging.getLogger(__name__)

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        return MessageSerializer

    def get_queryset(self):
        return MessageQueue.objects.none()
    
    @swagger_auto_schema(
        operation_description="Send message",
        operation_summary="Send sms",
        method="post",
        tags=["message"],
    )
    @action(detail=False, methods=['post'])
    def send_sms(self, request):
        try:
            client = MessageHttpClient(phone_number='+255717251140', text='This is test', reference='This is reference')
            
            response = client.send_sms()
            
            if response is None:
                return Response(data={"detail": "failed to send sms"}, status=status.HTTP_400_BAD_REQUEST)
            
            print(response)
            
            if response.status_code == 200:
                response_data = response.json()
                
                print(response_data)
        except Exception as e:
            logger.error(f"An error occured: {e}", exc_info=True)
            raise e