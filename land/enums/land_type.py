from enum import Enum

class LAND_TYPE(Enum):
    RESIDENTIAL = 'Makazi'
    COMMERCIAL = 'Biashara'
    AGRICULTURAL = 'Kilimo'
    VACANT = 'Tupu'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

    @classmethod
    def default(cls):
        return cls.RESIDENTIAL.name
