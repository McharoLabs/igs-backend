import logging

from payment.models import Payment


logger = logging.getLogger(__name__)

def auto_activate_account_job():
    try:
        Payment.auto_activate_account()
    except Exception as e:
        logger.error(f"Error expiring accounts: {e}", exc_info=True)
