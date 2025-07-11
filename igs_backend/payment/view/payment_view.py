from django.http import HttpResponse
from requests import Response
from rest_framework import permissions
from rest_framework.decorators import action
from igs_backend import settings
from message.utils import SmsService
from payment.enums.payment_type import PAYMENT_TYPE
from payment.models import Payment
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from utils.http_client import PaymentHttpClient
from requests.exceptions import RequestException, Timeout, ConnectionError
from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class PaymentWebHook(APIView):
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        if request.data:
            data = request.data
            try:
                logger.info(f"Webhook received data: {data}")
                order_id: str = data.get("order_id")

                client = PaymentHttpClient(base_url=settings.ZENOPAY_BASE)
                response: Response | None = client.check_order_status(order_id=order_id)

                if response is None:
                    return HttpResponse('Empty request body for status check after webhook call', 400)

                if response.status_code == 200:
                    response_data = response.json()
                    response_status: str = response_data.get("status")

                    if response_status.lower() == "error":
                        return HttpResponse(f"No order found with order id from status check {order_id}", 400)

                    sc_amount = response_data.get("amount")
                    sc_payment_status: str = response_data.get("payment_status")
                    wh_payment_status: str = data.get("payment_status")
                    wh_reference = data.get("reference")

                    wh_metadata = data.get("metadata") or {}
                    wh_payment_id = wh_metadata.get("payment_id")
                    wh_customer_name = wh_metadata.get("customer_name")
                    wh_customer_email = wh_metadata.get("customer_email")

                    if sc_payment_status.upper() == wh_payment_status.upper():
                        payment: Payment | None = Payment.get_payment_for_callback(payment_id=wh_payment_id, order_id=order_id)

                        if payment is None:
                            return HttpResponse(f"Order with id {order_id} not found", 400)

                        if Decimal(payment.amount) != Decimal(sc_amount):
                            return HttpResponse("Amount from order check status did not match with previous saved order amount", 400)

                        payment.on_complete_payment(
                            payment_status=sc_payment_status,
                            reference=wh_reference,
                            customer_email=wh_customer_email,
                            customer_name=wh_customer_name
                        )
                        
                        sms_service = SmsService(reference=wh_reference)
                        
                        if payment.payment_type == PAYMENT_TYPE.BOOKING.value:
                            sms_service.send_booking_message(
                                customer_name=wh_customer_name,
                                agent=payment.property.agent,
                                customer_phone=payment.phone_number
                            )

                        elif payment.payment_type == PAYMENT_TYPE.ACCOUNT.value:
                            sms_service.send_subscription_sms(
                                name = payment.property.agent.full_name,
                                reference = wh_reference,
                                subscription_plan = payment.plan
                            )

                        logger.info(f"Payment made successful for {payment}")
                        return HttpResponse("Success", 200)

                    return HttpResponse("Payment status does not match", 400)

            except (ValueError, KeyError, ValidationError) as e:
                logger.error(f"Error occurred: {e}", exc_info=True)
                return HttpResponse(f"Error: {str(e)}", status=400)

            except (RequestException, Timeout, ConnectionError) as e:
                logger.error(f"Network error occurred: {str(e)}", exc_info=True)
                return HttpResponse(f"Network error: {str(e)}", status=500)

            except APIException as e:
                logger.error(f"API exception occurred: {str(e)}", exc_info=True)
                return HttpResponse(f"API exception: {str(e)}", status=500)

            except Exception as e:
                logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
                return HttpResponse(f"Unexpected error: {str(e)}", status=500)

        return HttpResponse('Empty webhook body received', status=400)
