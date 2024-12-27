import logging
from account.model.account import Account
from house.model.house import House
from house.model.house_transaction import HouseTransaction

logger = logging.getLogger(__name__)
  
  
def my_scheduled_job():
    try:
        HouseTransaction.cron_house_complete_transaction()
        HouseTransaction.cron_room_complete_transaction(amount="90000")
    except Exception as e:
        logger.error(f"Error occurred while running cron job: {e}", exc_info=True)
        

def activate_house_job():
    try:
        active_accounts = Account.get_active_accounts()
        
        for active in active_accounts:
            if active.agent:
                House.activate_inactive_houses(agent=active.agent)
            if active.landlord:
                House.activate_inactive_houses(landlord=active.landlord)
    
    except Exception as e:
        logger.error(f"Error in the house activation job: {e}", exc_info=True)
        
def deactivate_house_job():
    try:
        active_accounts = Account.get_inactive_accounts()
        
        for active in active_accounts:
            if active.agent:
                House.deactivate_active_houses(agent=active.agent)
            if active.landlord:
                House.deactivate_active_houses(landlord=active.landlord)
    
    except Exception as e:
        logger.error(f"Error in the house deactivation job: {e}", exc_info=True)
