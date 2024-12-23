from django.db import models

from house.model.house_room import Room
from user.model.tenant import Tenant

class TenantRoom(models.Model):
    tenant_house_id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.RESTRICT, related_name="tenant_room")
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room")
    check_in_date = models.DateField(null=True, blank=True)
    check_out_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'tenant_room'
