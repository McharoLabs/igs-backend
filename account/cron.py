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
        client = MessageHttpClient()

        if accounts:
            for account in accounts:
                expired = account.expire_account()
                
                if expired:
                    reference = generate_short_reference()

                    message = (
                        f"Mpendwa {account.agent.full_name} ,\n"
                        "Akaunti yako imekwisha muda wake na haitatumika tena.\n"
                        "Tafadhali rejesha akaunti yako ili huduma ziendelee.\n"
                        "Mali zako hazitaonekana kwa wateja hadi akaunti iwe imerejeshwa.\n"
                        f"Ingia kwenye {settings.WEB_URL}, nenda Mipangilio > Akaunti,\n"
                        "chagua mpango unaotaka na fanya malipo ili kuendelea kutumia huduma."
                    )
                    


                    response = client.send_to_single_destination(
                        phone_number=f"255{account.agent.phone_number[1:]}",
                        message=message,
                        reference=reference
                    )


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
                message=(
                    f"Mpendwa {agent.full_name},\n"
                    "Umepewa usajili wa akaunti ya bure.\n"
                    "Akaunti hii ina baadhi ya vikwazo:\n"
                    "\t1: Inapewa kipaumbele cha mwisho kwenye ukurasa wa mbele wa mteja na kwenye utafutaji.\n"
                    f"Ikiwa unahitaji kuwa na kipaumbele cha kwanza, tafadhali ingia kwenye {settings.WEB_URL},\n"
                    "nenda Mipangilio > Akaunti, chagua mpango na fanya malipo."
                ),
                reference=reference
            )
        
    except Exception as e:
        logger.error(f"Subscription of free account error: {e}", exc_info=True)