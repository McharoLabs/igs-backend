from enum import Enum

class PaymentStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

    @classmethod
    def choices(cls):
        return [(status, status.value) for status in cls]
    
    @classmethod
    def default(cls) -> str:
        return cls.PENDING.value