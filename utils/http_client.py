# utils/http_client.py

import json
import requests
from requests import Response
from requests.exceptions import HTTPError, Timeout
from typing import Optional, Dict, Any, Union
from tenacity import retry, stop_after_attempt, wait_exponential
import logging

logger = logging.getLogger(__name__)


class HttpClient:
    """Make requests to payment gate-way
    """
    _order_status_endpoint = "order-status"

    def __init__(
        self,
        base_url: str,
        timeout: Optional[int] = 10,
        max_retries: int = 3,
        retry_wait_multiplier: int = 1
    ) -> None:
        """Initialize properties

        Args:
            base_url (str): Base url of the endpoint
            timeout (Optional[int], optional): Time out in minutes for the retry. Defaults to 10.
            max_retries (int, optional): Maximum number of retries on failure. Defaults to 3.
            retry_wait_multiplier (int, optional): Retry wait multiplier. Defaults to 1.
        """
        self.base_url: Optional[str] = base_url.rstrip("/")
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
        """Make request for the payment

        Args:
            url (Optional[str], optional): Expected endpoint after the base url. Defaults to None.
            data (Optional[Union[Dict[str, Any], str]], optional): Data to be posted to the payment gateway. Defaults to None.

        Returns:
            Response: Response ffrom the payment gateway
        """
        
        url = f"{self.base_url}/{url}" if url else self.base_url
        response: Response = requests.post(url=url, data=data)
            
        response.raise_for_status()
        payment_data = {
            "status_code": response.status_code,
            "data": response.text,
        }
        logger.info(f"Payment request response: {payment_data}")
        return response
    
    @retry(
        stop=stop_after_attempt(3),  
        wait=wait_exponential(multiplier=1, min=1, max=10),  
        retry=(lambda retry_state: isinstance(retry_state.outcome.exception(), Timeout))
    )
    def check_order_status(self, *, data: Dict[str, Any]) -> Response:
        """Check for the payment status after push

        Args:
            data (Dict[str, Any]): Data to be posted to check for the payment status

        Returns:
            Response: Response from the payment gateway for status check
        """
        response: Response = requests.post(url=f"{self.base_url}/{self._order_status_endpoint}", data=data)
        payment_data = {
            "status_code": response.status_code,
            "data": response.text,
        }
        logger.info(f"Payment status check response: {payment_data}")
        response.raise_for_status()
        return response
    
    