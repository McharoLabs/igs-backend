from account.models import Account
from property.models import Property
import logging

logger = logging.getLogger(__name__)


def deactivate_property_job():
    try:
        accounts = Account.get_inactive_accounts()
        
        for account in accounts:
            active = Account.get_account(agent=account.agent)
            
            if active is None:
                Property.deactivate_active_properties(agent=account.agent)

    except Exception as e:
        logger.error(f"Error in the property deactivation job: {e}", exc_info=True)
        

def activate_property_job():
    try:
        accounts = Account.get_active_accounts()
        
        for account in accounts:
            
            Property.activate_inactive_properties(agent=account.agent)
            

    except Exception as e:
        logger.error(f"Error in the property activation job: {e}", exc_info=True)
