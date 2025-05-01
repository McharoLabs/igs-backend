from enum import Enum

class LandSizeType(Enum):
    SQUARE_METERS = 'Mita za Mraba (m²)'
    HECTARES = 'Hekta (ha)'
    SQUARE_FEET = 'Futi za Mraba (sq ft)'
    ACRES = 'Ekari (ac)'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def default(cls):
        return cls.SQUARE_METERS.name