from enum import Enum
from typing import List, Tuple

class SECURITY_FEATURES(Enum):
    CCTV = 'CCTV'
    GATED_COMMUNITY = 'Gated Community'
    ALARM_SYSTEM = 'Alarm System'
    SECURITY_GUARD = 'Security Guard'
    INTERCOM = 'Intercom'
    FENCED = 'Fenced'
    ELECTRONIC_GATE = 'Electronic Gate'
    OTHERS = 'Others'

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(key.value, key.value) for key in cls]
    
    @classmethod
    def default(cls) -> str:
        return cls.OTHERS.value
