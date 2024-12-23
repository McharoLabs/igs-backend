from enum import Enum
from typing import List, Tuple


class ROOM_STATUS(Enum):
    AVAILABLE = 'Available'
    BOOKED = 'Booked'
    RENTED = 'Rented'
    
    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(status.value, status.value) for status in cls]
    
    @classmethod
    def default(cls) -> str:
        return cls.AVAILABLE.value