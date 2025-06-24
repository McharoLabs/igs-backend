from enum import Enum

class LAND_STATUS(Enum):
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    RENTED = 'Rented'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def default(cls):
        return cls.AVAILABLE.name
