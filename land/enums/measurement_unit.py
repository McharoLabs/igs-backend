from enum import Enum

class LAND_MEASUREMENT_UNIT(Enum):
    SQUARE_METERS = 'Square meters'
    ACRES = 'Acres'
    HECTARES = 'Hectares'

    @classmethod
    def choices(cls):
        return [(unit.name, unit.value) for unit in cls]

    @classmethod
    def default(cls):
        return cls.SQUARE_METERS.name
