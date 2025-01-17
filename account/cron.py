import logging

from account.models import Account

logger = logging.getLogger(__name__)

def expire_account_job():
    try:
        accounts = Account.get_active_accounts()
        
        if accounts:
            for account in accounts:
                account.expire_account()
    
    except Exception as e:
        logger.error(f"Error expiring accounts: {e}", exc_info=True)
