import uuid
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


import logging


logger = logging.getLogger(__name__)

class SiteSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    support_phone = models.CharField(max_length=100, null=False, blank=False)
    support_email = models.CharField(max_length=100, null=False, blank=False)
    headquarters = models.CharField(max_length=255, null=False, blank=False)
    booking_fee = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'settings'
        app_label = 'settings'
        
    
    def save(self, *args, **kwargs):
        # Ensure only one row exists in the table
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("Only one settings row is allowed.")
        super(SiteSettings, self).save(*args, **kwargs)
    
    @classmethod
    def get_company_settings(cls) -> 'SiteSettings | None':
        """Retrive company information

        Returns:
            Settings | None: Company information if found, Otherwise None
        """
        return cls.objects.filter().first()