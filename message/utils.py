import logging
from typing import Any, List, Dict

from requests import Response
from account.models import Account
from igs_backend import settings
from settings.models import SiteSettings
from subscription_plan.models import SubscriptionPlan
from user.model.agent import Agent
from utils.http_client import MessageHttpClient
from message.models import MessageQueue

logger = logging.getLogger(__name__)


class SmsService:
    def __init__(self, reference: str = None):
        self.__reference = reference
        self.__client = MessageHttpClient()
        self.__company_info = SiteSettings()
        
    def send_message(self, message: str, phone_number: str) -> None:
        self.__send_message(message=message, phone_number=phone_number)
        
    def send_booking_message(self, customer_name: str, customer_phone: str, agent: Agent) -> None:
        self.__send_booking_tenant_message(
            name=customer_name,
            phone_number=customer_phone,
            agent_phone=agent.phone_number,
            agent_name=agent.full_name
        )
        self.__send_booking_agent_message(
            customer_name=customer_name,
            customer_phone=customer_phone,
            agent=agent
        )
        
    def __send_booking_tenant_message(self, name: str, phone_number: str, agent_phone: str, agent_name: str) -> None:
        message = f"""
        Salamu kwako ndugu {name}\n\n
        Namba ya simu ya mali wa mali ni {agent_phone}\n\n
        Kuboresha huduma yetu kwa kujulikana, tafadhali wataarifu ndugu jamaa na marafiki kutembelea {settings.WEB_URL} kuona mali mbali mbali
        """
        
        self.__send_message(message=message, phone_number=phone_number)
        
    def __send_booking_agent_message(self, customer_name: str, customer_phone: str, agent: Agent) -> None:
        message = f"""
        Salamu kwako ndugu {agent.full_name}\n\n
        Mteja umepata mteja aliyependezwa na mali yako mwenye taarifa\n
        Jina: {customer_name}\n
        Number ya simu: {customer_phone}\n\n
        Kama hajakutafuta, tafadhali mtafute kuogeza uaminifu\n
        Kurudisha mali yako hewani tembelea {settings.WEB_URL} -> Dashibodi -> Tafuta mali kwa jina {customer_name} -> Tazama zaid
        """
        
        self.__send_message(message=message, phone_number=agent.phone_number)
        
    def send_subscription_sms(self, name: str, reference: str, phone_number: str, subscription_plan: SubscriptionPlan) -> None:
        message = f"""
        Salamu kwako ndugo {name}\n\n
        Umefanikisha kujiunga na plani {subscription_plan.name}\n\n
        Jina la plani: {subscription_plan.name}\n
        muda wa plani: {subscription_plan.duration_days}\n
        Idadi ya mali: {subscription_plan.max_houses}\n
        Kiasi: {subscription_plan.price}\n
        Numbari ya rejea: {reference}\n\n
        Kwa msaada piga simu: {self.__company_info.support_phone}\n
        Barua pepe: {self.__company_info.support_email}\n\n
        Tembelea {settings.WEB_URL} kutangana nasi.\n\n
        """
        self.__send_message(message=message, phone_number=phone_number)
        
    def __send_message(self, message: str, phone_number: str) -> None:
        """Send message to a single destination."""
        
        phone_number = f"{settings.COUNTRY_CODE}{phone_number[1:]}"
        
        try:
            response = self.__client.send_to_single_destination(phone_number=phone_number, message=message, reference=self.__reference)
            
            if response is None:
                logger.error("Failed to send SMS", exc_info=True)
                return
            
            if response.status_code == 200:
                self.__handle_response(response=response)
            else:
                logger.error(f"Error fetching the delivery report: Status Code {response.status_code}")
        except Exception as e:
            logger.error(f"An error occurred while sending the SMS: {e}", exc_info=True)
    
    def __handle_response(self, response: Response) -> None:
        """Handle and process the SMS reponse."""

        response_data: Dict[str, List[Dict[str, Any]]] = response.json()
        messages = response_data.get("messages", [])
        
        if messages:
            for message in messages:
                self.__save_message(message=message)
        else:
            logger.error("No messages found in the response")
    
    def __save_message(self, message: Dict) -> None:
        """Save the message information into the database."""
        
        to = message.get("to")
        
        to = message.get("to")
        message_id = message.get("messageId")
        message_text = message.get("message")

        message_status: Dict[str, Any] = message.get("status", {})
        group_name = message_status.get("groupName")
        name = message_status.get("name")
        description = message_status.get("description")
        
        MessageQueue.save_message(
            message=message_text, 
            phone_number=to, 
            message_id=message_id,
            group_name=group_name,
            name=name,
            description=description,
            reference=self.__reference,
        )
        logger.info(f"Message sent successfully to {to} with Message ID: {message_id}")


def subscribe(agent: Agent, subscription_plan: SubscriptionPlan = None) -> None:
    client = SmsService()

    try:
        if subscription_plan is None:
            subscription_plan = SubscriptionPlan.get_free_plan()

            if subscription_plan is None:
                logger.error(f"No free subscription plan available for agent {agent.full_name}.")
                return

        Account.subscribe_free_account(plan=subscription_plan, agent=agent)

        message = f"""
        Samalu kwako ndugo {agent.full_name}\n\n
        Umepewa akaunti ya bure kutoka Kedesh\n
        Akaunti hii haitoi vipaumbele kwenye mali zako, hivyo zitakua zamwisho kuonekana kwa wateja\n\n
        Kulipia plani mpya tembelea {settings.WEB_URL} -> Mipangilio -> Profile, Chagua plani ili mali zako zipewe kipaumbele.\n\n

        Kampuni: Kedesh Limited\n
        Website: {settings.WEB_URL}
        """

        try:
            client.send_message(message=message, phone_number=agent.phone_number)
        except Exception as sms_error:
            logger.error(f"Failed to send SMS to {agent.phone_number}: {sms_error}")

    except Exception as e:
        logger.error(f"Error subscribing agent {agent.full_name}: {e}", exc_info=True)
        raise e



def send_sms(message: str, phone_number: str) -> None:
    client = SmsService()

    try:
        client.send_message(message=message, phone_number=phone_number)
    except Exception as e:
        logger.error(f"Failed to send SMS to {phone_number}: {e}", exc_info=True)
        return None
