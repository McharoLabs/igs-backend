from .user import User

class Tenant(User):
    pass
    class Meta:
        db_table = 'tenant'