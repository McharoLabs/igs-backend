from django.db import models

from house.model.house_transaction import HouseTransaction
from user.model.tenant import Tenant

class HouseTenant(models.Model):
    house_tenant_id = models.AutoField(primary_key=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="house_tenants")
    transaction = models.ForeignKey(HouseTransaction, on_delete=models.CASCADE, related_name="house_tenants")
    tenant_in_date = models.DateField()
    tenant_out_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'house_tenant'
