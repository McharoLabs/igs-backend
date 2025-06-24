import logging
import uuid
from settings.models import SiteSettings
from utils.http_client import MessageHttpClient

logger = logging.getLogger(__name__)

def generate_short_reference():
    return str(uuid.uuid4())[:8]

def check_message_balance_job():
    try:
        client = MessageHttpClient()
        
        response = client.message_balance()
            
        if response.status_code == 200:
            response_json = response.json()
                
            sms_balance = response_json.get("sms_balance")
                
                
            if isinstance(sms_balance, str):
                try:
                        
                    sms_balance = int(sms_balance)
                    
                    reference = generate_short_reference()
                    
                    if sms_balance <= 30:
                        logger.debug(f"Raw SMS Balance: {sms_balance}")
                        
                        siteInfo = SiteSettings.company_settings()
                        
                            
                        message = f"Akaunti yako ya NextSMS imebakiwa na meseji {sms_balance}, tafadhali ongeza meseji kabla hazijaisha kuepusha usumbufu kwa wateja kukosa meseji kwa wakati"
                        res = client.send_to_single_destination(phone_number=f"255{siteInfo.support_phone[1:]}", message=message, reference=reference)
                            
                except ValueError:
                    logger.error(f"Failed to convert sms_balance to an integer: {sms_balance}")
                    sms_balance = 0
            elif not isinstance(sms_balance, int):
                logger.error(f"Unexpected sms_balance type: {type(sms_balance)}")
                sms_balance = 0
        else:
            logger.error(f"Failed to retrieve message balance. Status code: {response.status_code}")
        
    except Exception as e:
        logger.error(f"An error occurred while getting the message balance: {str(e)}")