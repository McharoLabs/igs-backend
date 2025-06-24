from enum import Enum
from typing import List, Tuple

class HEATING_COOLING_SYSTEM(Enum):
    CENTRAL_HEATING = 'Central Heating'
    AIR_CONDITIONING = 'Air Conditioning'
    UNDERFLOOR_HEATING = 'Underfloor Heating'
    HEAT_PUMP = 'Heat Pump'
    RADIATORS = 'Radiators'
    FAN_COOLING = 'Fan Cooling'
    NONE = 'None'

    @classmethod
    def choices(cls) -> List[Tuple[str, str]]:
        return [(key.value, key.value) for key in cls]
    
    @classmethod
    def default(cls) -> str:
        return cls.NONE.value
