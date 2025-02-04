from enum import Enum

class PaymentType(Enum):
    BOOKING = 'Booking'
    ACCOUNT = 'Account'

    @classmethod
    def choices(cls):
        return [(status, status.value) for status in cls]
    
    @classmethod
    def default(cls) -> str:
        return cls.BOOKING.value