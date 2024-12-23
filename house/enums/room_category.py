from enum import Enum
from typing import List, Tuple

class ROOM_CATEGORY(Enum):
    SELF_CONTAINED = 'Self-contained'
    SHARED = 'Shared'
    SINGLE_ROOM = 'Single Room'
    DOUBLE_ROOM = 'Double Room'
    MASTER_ROOM = 'Master Room'
    ENSUITE = 'En-suite'
    COMMON_ROOM = 'Common Room'
    STUDIO = 'Studio'
    BUNK_ROOM = 'Bunk Room'

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(key.value, key.value) for key in cls]
    
    @classmethod
    def default(cls) -> str:
        return cls.SELF_CONTAINED.value
