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
    
    @classmethod
    def valid(cls, category:str) -> bool:
        if category not in [choice[0] for choice in cls.choices()]:
            return False
        return True