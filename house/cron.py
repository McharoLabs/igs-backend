import logging
from account.models import Account
from property.models import Property
logger = logging.getLogger(__name__)

def activate_house_job():
    try:
        accounts = Account.get_active_accounts()
        
        for account in accounts:
            Property.activate_inactive_properties(agent=account.agent)
    
    except Exception as e:
        logger.error(f"Error in the property activation job: {e}", exc_info=True)

