import logging
from typing import Any
from igs_backend.igs_backend import settings
from payment.enums.payment_type import PAYMENT_TYPE
from payment.models import Payment
from user.model.agent import Agent
from utils.http_client import MessageHttpClient
from message.models import MessageQueue

logger = logging.getLogger(__name__)
