from enum import Enum
from typing import List, Tuple

class FURNISHING_STATUS(Enum):
    FULLY_FURNISHED = 'Fully Furnished'
    PARTIALLY_FURNISHED = 'Partially Furnished'
    UNFURNISHED = 'Unfurnished'

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(status.value, status.value) for status in cls]

    @classmethod
    def default(cls) -> str:
        return cls.UNFURNISHED.value    
