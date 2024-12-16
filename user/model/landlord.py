from .user import User

class Landlord(User):
    pass
    class Meta:
        db_table = 'landlord'