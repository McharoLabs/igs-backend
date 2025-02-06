import logging
from .models import Payment

logger = logging.getLogger(__name__)

def delete_pending_payments_job():
    try:
        Payment.delete_pending_payments()
    
    except Exception as e:
        logger.error(f"Error while deleting pending payments job: {e}", exc_info=True)
