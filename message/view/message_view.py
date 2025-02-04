import logging
from typing import Any
from igs_backend import settings
from payment.enums.payment_type import PaymentType
from payment.models import Payment
from utils.http_client import MessageHttpClient
from message.models import MessageQueue

logger = logging.getLogger(__name__)

class MessageUtility:
    _client = MessageHttpClient()

    def __init__(self,reference: str, customer_name: str, payment: Payment):
        self._reference = reference
        self._payment = payment
        self._customer_name = customer_name

    def send_sms(self) -> None:
        if self._payment.payment_type == PaymentType.ACCOUNT.value:
            agent_message = f"You have successful subscribed {self._payment.plan.name}\nReference: {self._reference}\nAmount: {self._payment.amount}\nLogin to upload property at {settings.WEB_URL}"
            self._single_destination(message=agent_message, phone_number=f"255{self._payment.phone_number[1:]}")
        else:
            agent_message = f"Dear {self._payment.agent.first_name} {self._payment.agent.last_name} you have new booking from {self._customer_name}\nContact: {self._payment.phone_number}"
            tenant_message = f"Dear {self._customer_name} you have successful booked the property.\nAgent: {self._payment.property.agent.first_name} {self._payment.property.agent.middle_name} {self._payment.property.agent.last_name} {self._customer_name}\nContact: {self._payment.phone_number}"
            data = {
                "messages": [
                    {"from": settings.MESSAGE_FROM, "to": f"255{self._payment.phone_number[1:]}", "text": tenant_message},
                    {"from": settings.MESSAGE_FROM, "to": f"255{self._payment.agent.phone_number[1:]}", "text": agent_message}
                ],
                "reference": self._reference
            }
            self._multiple_destination(data=data)

    def _single_destination(self, message: str, phone_number: str):
        try:
            response = self._client.send_to_single_destination(phone_number=phone_number, message=message, reference=self._reference)
            
            if response is None:
                logger.error("Failed to send SMS: No response received.")
                return None

            if response.status_code == 200:
                response_data = response.json()
                messages = response_data.get("messages", [])
                
                if messages:
                    first_message = messages[0]
                    to = first_message.get("to")
                    message_id = first_message.get("messageId")
                    message_text = first_message.get("message")
                    
                    message_status = first_message.get("status", {})
                    group_name = message_status.get("groupName")
                    name = message_status.get("name")
                    description = message_status.get("description")
                    
                    MessageQueue.save_message(
                        payment=self._payment,
                        message=message_text, 
                        phone_number=to, 
                        message_id=message_id,
                        group_name=group_name,
                        name=name,
                        description=description,
                    )
                    logger.info(f"Message sent successfully to {to} with Message ID: {message_id}")
                else:
                    logger.error("No messages found in the response")
            else:
                logger.error(f"Error fetching the delivery report: Status Code {response.status_code}")
        
        except Exception as e:
            logger.error(f"An error occurred while sending the SMS: {e}", exc_info=True)

        return None
    
    def _multiple_destination(self, data: Any):
        try:
            response = self._client.send_to_multi_destination(data=data)

            if response is None:
                logger.error("Failed to send SMS: No response received.")
                return None

            if response.status_code == 200:
                response_data = response.json()
                messages = response_data.get("messages", [])

                if messages:
                    for message in messages: 
                        to = message.get("to")
                        message_id = message.get("messageId")
                        message_text = message.get("message")

                        message_status = message.get("status", {})
                        group_name = message_status.get("groupName")
                        name = message_status.get("name")
                        description = message_status.get("description")

                        MessageQueue.save_message(
                            payment=self._payment,
                            message=message_text, 
                            phone_number=to, 
                            message_id=message_id,
                            group_name=group_name,
                            name=name,
                            description=description,
                        )
                        logger.info(f"Message sent successfully to {to} with Message ID: {message_id}")
                else:
                    logger.error("No messages found in the response")
            else:
                logger.error(f"Error fetching the delivery report: Status Code {response.status_code}")

        except Exception as e:
            logger.error(f"An error occurred while sending the SMS: {e}", exc_info=True)

        return None

