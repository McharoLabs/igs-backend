import base64
import requests
from requests import Response
from requests.exceptions import Timeout, RequestException
from typing import Optional, Dict, Any, Union
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from igs_backend import settings


logger = logging.getLogger(__name__)

class PaymentHttpClient:
    _order_status_endpoint = "order-status"

    def __init__(
        self,
        base_url: str,
        timeout: Optional[int] = 10,
        max_retries: int = 3,
        retry_wait_multiplier: int = 1
    ) -> None:
        self.base_url: str = base_url.rstrip("/")
        self.timeout: int = timeout
        self.max_retries: int = max_retries
        self.retry_wait_multiplier: int = retry_wait_multiplier

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(lambda retry_state: isinstance(retry_state.outcome.exception(), Timeout))
    )
    def make_payment(
        self,
        url: Optional[str] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
    ) -> Response:
        url = f"{self.base_url}/{url}" if url else self.base_url
        try:
            response: Response = requests.post(url=url, data=data, timeout=self.timeout)
            response.raise_for_status()
            payment_data = {
                "status_code": response.status_code,
                "data": response.text,
            }
            logger.info(f"Payment request response: {payment_data}")
            return response
        except RequestException as e:
            logger.error(f"Error in payment request: {e}", exc_info=True)
            return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(lambda retry_state: isinstance(retry_state.outcome.exception(), Timeout))
    )
    def check_order_status(self, order_id: str)  -> Response:
        status_data = {
            'order_id': order_id,
            'api_key': settings.ZENOPAY_API_KEY,
            'secret_key': settings.ZENOPAY_SECRET_KEY,
        }

        try:
            response: Response = requests.post(
                url=f"{self.base_url}/{self._order_status_endpoint}",
                data=status_data,
                timeout=self.timeout
            )
            logger.info(f"Satus check response: {response.text}")
            response.raise_for_status()
            return response
        except RequestException as e:
            logger.error(f"Error fetching order status: {e}", exc_info=True)
            return None
        
        
class MessageHttpClient:
    _base_url = settings.MESSAGE_BASE_URL
    _single_sms_url = settings.MESSAGE_SINGLE_URL
    _multi_sms_url = settings.MESSAGE_MULTI
    _derivery_report = f"{_base_url}/{settings.DERIVERY_REPORT_URL}=" 
    _from = settings.MESSAGE_FROM
        
    def _generate_message_basic_auth_header(self) -> str:
        """Generate basic authorization header for the message by encoding to Base64 username and password of format (username:password)

        Returns:
            str: Authoriation header of format (Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==)
        """

        combined = f"{settings.MESSAGE_USERNAME}:{settings.MESSAGE_PASSWORD}"
        
        encoded = base64.b64encode(combined.encode('utf-8')).decode('utf-8')
        
        authorization_header = f"Basic {encoded}"
        print(authorization_header)
        return authorization_header

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(lambda retry_state: isinstance(retry_state.outcome.exception(), Timeout))
    )
    def send_to_single_destination(self, phone_number: str, message: str, reference: str) -> Response:
        headers = {
            "Authorization": self._generate_message_basic_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        data = {
            "from": self._from,
            "to": phone_number,
            "text": message,
            "reference": reference
        }

        try:
            response: Response = requests.post(
                url=f"{self._base_url}/{self._single_sms_url}",
                json=data, 
                headers=headers,
                timeout=10  
            )
            response.raise_for_status() 
            logger.info(f"Message sent successfully: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending SMS: {e}", exc_info=True)
            return None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=(lambda retry_state: isinstance(retry_state.outcome.exception(), Timeout))
    )
    def send_to_multi_destination(self, data: Any) -> Response:
        headers = {
            "Authorization": self._generate_message_basic_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        try:
            response: Response = requests.post(
                url=f"{self._base_url}/{self._multi_sms_url}",
                json=data, 
                headers=headers,
                timeout=10  
            )
            response.raise_for_status() 
            logger.info(f"Message sent successfully: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending SMS: {e}", exc_info=True)
            return None
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=lambda retry_state: isinstance(retry_state.outcome.exception(), Timeout)
    )
    def report(self, message_id: str) -> Response | None:
        """Fetch SMS delivery report for a given message ID."""
        headers = {
            "Authorization": self._generate_message_basic_auth_header(),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = f"{self._base_url}{message_id}"
        
        try:
            response: Response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Delivery report retrieved successfully: {response.text}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching delivery report: {e}", exc_info=True)
            return None