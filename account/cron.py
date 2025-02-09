import logging
import uuid

from account.models import Account
from igs_backend import settings
from message.view.message_view import MessageUtility
from subscription_plan.models import SubscriptionPlan
from utils.http_client import MessageHttpClient

logger = logging.getLogger(__name__)
def generate_short_reference():
    return str(uuid.uuid4())[:8]

def expire_account_job():
    try:
        accounts = Account.get_active_accounts()
        
        if accounts:
            for account in accounts:
                account.expire_account()
    
    except Exception as e:
        logger.error(f"Error expiring accounts: {e}", exc_info=True)

def subscribe_free_account_job():
    try:
        client = MessageHttpClient()
        
        free_plan = SubscriptionPlan.get_free_plan()
        
        if free_plan is None:
            return None
        
        agents = Account.get_agents_without_account()
        
        for agent in agents:
            Account.subscribe_free_account(plan=free_plan, agent=agent)
            
            reference = generate_short_reference()

            response = client.send_to_single_destination(
                phone_number=f"255{agent.phone_number[1:]}",
                message=f"Dear {agent.first_name} {agent.middle_name} {agent.last_name}\nYou have free account subscription, please login to {settings.WEB_URL} to upload your property",
                reference=reference
            )
        
        
    except Exception as e:
        logger.error(f"Subscription of free account error: {e}", exc_info=True)