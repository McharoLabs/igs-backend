from enum import Enum
from typing import List, Tuple


class GENDER(Enum):
    MALE = 'Male'
    FEMALE = 'Female'
    
    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(g.value, g.value) for g in cls]