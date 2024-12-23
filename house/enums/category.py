from enum import Enum


class CATEGORY(Enum):
    RENTAL = "Rental"
    SALE = "Sale"

    @classmethod
    def choices(cls):
        return [(tag.value, tag.value) for tag in cls]
    
    @classmethod
    def default(cls):
        return cls.RENTAL.value