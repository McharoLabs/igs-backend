from enum import Enum

class PAYMENT_TYPE(Enum):
    BOOKING = 'Booking'
    ACCOUNT = 'Account'
    NONE = 'None'

    @classmethod
    def choices(cls):
        return [(status, status.value) for status in cls]
    
    @classmethod
    def default(cls) -> str:
        return cls.BOOKING.value