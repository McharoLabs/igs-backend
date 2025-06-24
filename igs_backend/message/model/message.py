import uuid
from django.db import models

from payment.models import Payment
from utils.phone_number import validate_phone_number

class MessageQueue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField()
    to = models.CharField(max_length=20, validators=[validate_phone_number], null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)
    reference = models.CharField(null=True, max_length=100)

    class Meta:
        db_table = 'message_quue'
        app_label = 'message'
        
    def __str__(self) -> str:
        return str(self.message_id)
    
    @classmethod
    def save_message(cls, message: str, phone_number: str, message_id: str, description: str = None, name: str = None, group_name: str = None, reference: str = None) -> None:
        message_obj = cls(
            message=message,
            to=phone_number,
            message_id=message_id,
            description=description,
            name=name,
            group_name=group_name,
            reference = reference,
        )
        message_obj.save()
