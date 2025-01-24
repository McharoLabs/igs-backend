from django.http import HttpRequest, HttpResponse
from rest_framework import permissions
from rest_framework.decorators import action
import logging

from payment.models import Payment
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)

class PaymentWebHook(APIView):

    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        
        if request.data:
            data = request.data
            # data = request.data.decode('utf-8')
            
            try:
                logger.info(f"Webhook received data: {data}")
                # Payment.on_complete_payment(payment_status=data.payment_status, reference=data.reference)
            except:
                return HttpResponse('An error occurred processing the webhook data.', status=400)
        return HttpResponse('Empty request body.', status=400)