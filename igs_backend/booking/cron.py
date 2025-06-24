import logging

from booking.models import Booking

logger = logging.getLogger(__name__)
  
  
def my_scheduled_job():
    try:
        print("cron")
    except Exception as e:
        logger.error(f"Error occurred while running cron job: {e}", exc_info=True)
        