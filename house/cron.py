import logging
from house.model.house_transaction import HouseTransaction

logger = logging.getLogger(__name__)
  
  
def my_scheduled_job():
    try:
        HouseTransaction.cron_house_complete_transaction()
        HouseTransaction.cron_room_complete_transaction()
    except Exception as e:
        logger.error(f"Error occurred while running cron job: {e}", exc_info=True)