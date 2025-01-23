import json
import requests
from requests import Response
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Optional, Dict, Any, Union
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from igs_backend import settings

logger = logging.getLogger(__name__)

class HttpClient:
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
            response.raise_for_status()
            return response
        except RequestException as e:
            logger.error(f"Error fetching order status: {e}", exc_info=True)
            return None