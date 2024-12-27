import logging

from account.model.account import Account

logger = logging.getLogger(__name__)

def expire_account_job():
    try:
        accounts = Account.get_active_accounts()
        
        if accounts:
            logger.info(f"Trying to expire account(s) for: {[account for account in accounts]}")
            
            for account in accounts:
                account.expire_account()
        else:
            logger.info("No active accounts found to expire.")
    
    except Exception as e:
        logger.error(f"Error expiring accounts: {e}", exc_info=True)
