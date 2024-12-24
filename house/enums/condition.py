from enum import Enum


class CONDITION(Enum):
    USED = "Used"
    NEW = "New"
    RENOVATED = "Renovated"
    UNDER_CONSTRUCTION = "Under Construction"

    @classmethod
    def choices(cls):
        return [(tag.value, tag.value) for tag in cls]

    @classmethod
    def default(cls):
        return cls.USED.value
    
    @classmethod
    def valid(cls, condition:str) -> bool:
        if condition not in [choice[0] for choice in cls.choices()]:
            return False
        return True