import logging
import time

from account.models import Account
from message.utils import send_sms, subscribe

logger = logging.getLogger(__name__)

def expire_account_job():
    try:
        accounts = Account.get_active_accounts()

        if accounts:
            for account in accounts:
                expired = account.expire_account()

                if expired:
                    message = f"""
                    Salamu kwako ndugu {account.agent.full_name},\n\n
                    Plani yako {account.plan.name} imekwisha muda wake\n
                    Utapewa akaunti ya bure hivi punde\n
                    """
                    try:
                        send_sms(message=message, phone_number=account.agent.phone_number)
                    except Exception as sms_error:
                        logger.error(f"Failed to send SMS to {account.agent.phone_number}: {sms_error}")

                    time.sleep(10)
                    
                    try:
                        subscribe(agent=account.agent)
                    except Exception as subscribe_error:
                        logger.error(f"Failed to subscribe agent {account.agent.full_name}: {subscribe_error}")

    except Exception as e:
        logger.error(f"Error expiring accounts: {e}", exc_info=True)



def subscribe_free_account_job():
    try:
        agents = Account.get_agents_without_account()
        
        for agent in agents:
            subscribe(agent=agent)
        
    except Exception as e:
        logger.error(f"Subscription of free account error: {e}", exc_info=True)
