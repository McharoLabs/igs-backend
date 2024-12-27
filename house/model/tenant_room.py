from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
from house.enums.availability_status import STATUS
from house.model.house_room import Room
from user.model.tenant import Tenant
from django.db import transaction
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from utils.calculate_checkout_dat import calculate_checkout_date

class TenantRoom(models.Model):
    tenant_house_id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, related_name="tenant_room")
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room")
    check_in_date = models.DateField(default=timezone.now, editable=False)
    check_out_date = models.DateField(null=False, blank=False, editable=False)

    class Meta:
        db_table = 'tenant_room'
        
    @classmethod
    def tenant_in(cls, amount: Decimal, tenant: Tenant = None, room: Room = None) -> None:
        if tenant is None or room is None:
            raise ValidationError("Tenant and room are required.")
        
        try:
            room_instance = Room.get_room(room_id=room.room_id)
            
            if room_instance is None:
                raise ValidationError("Room not found")
            
            check_out_date = calculate_checkout_date(amount, room_instance.price)
            
            with transaction.atomic():
                take_in = cls(
                    tenant=tenant,
                    room=room,
                    check_out_date=check_out_date
                )
                take_in.save()

                room_instance.mark_rented()
                
        except ValidationError as e:
            raise ValidationError(f"Error during tenant check-in: {e}")
