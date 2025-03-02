from enum import Enum
from typing import List, Tuple

class RENTAL_DURATION(Enum):
    ONE_DAY = "1 Day"
    TWO_DAY = "2 Days"
    THREE_DAY = "3 Days"
    ONE_WEEK = "1 Week"
    TWO_WEEK = "2 Weeks"
    THREE_WEEK = "3 Weeks"
    ONE_MONTH = "1 Month"
    THREE_MONTHS = "3 Months"
    SIX_MONTHS = "6 Months"
    ONE_YEAR = "1 Year"

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(duration.value, duration.value) for duration in cls]

    @classmethod
    def default(cls) -> str:
        return cls.ONE_MONTH.value
