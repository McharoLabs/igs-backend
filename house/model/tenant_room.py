from django.db import models
from django.core.exceptions import ValidationError
from house.model.house_room import Room
from user.model.tenant import Tenant
from django.db import transaction

class TenantRoom(models.Model):
    tenant_house_id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, related_name="tenant_room")
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room")
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tenant_room'
        
    @classmethod
    def tenant_in(cls, tenant: Tenant = None, room: Room = None) -> None:
        if tenant is None or room is None:
            raise ValidationError("Tenant and room are required.")
        
        try:
            with transaction.atomic():
                take_in = cls(
                    tenant=tenant,
                    room=room
                )
                take_in.save()

                Room.mark_rented(room_id=room.room_id)
                
        except ValidationError as e:
            raise ValidationError(f"Error during tenant check-in: {e}")
