from enum import Enum

class ZONING_TYPE(Enum):
    RESIDENTIAL = 'Eneo la makazi'
    COMMERCIAL = 'Eneo la biashara'
    INDUSTRIAL = 'Eneo la viwanda'
    MIXED_USE = 'Matumizi mchanganyiko'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def default(cls):
        return cls.RESIDENTIAL.name
