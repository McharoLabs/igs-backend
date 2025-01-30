import uuid
from django.db import models

from payment.models import Payment
from utils.phone_number import validate_phone_number

class MessageQueue(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="messages", null=False)
    message = models.TextField()
    to = models.CharField(max_length=20, validators=[validate_phone_number], null=False, blank=False)
    description = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    group_name = models.CharField(max_length=100, null=True, blank=True)
    
    
    class Meta:
        db_table = 'message_quue'
        app_label = 'message'
        
    def __str__(self) -> str:
        return str(self.message_id)
    
    @classmethod
    def save_message(cls, payment: Payment, message: str, phone_numer: str) -> None:
        message = cls(
            payment=payment,
            messae=message,
            to=phone_numer,
        )
        
        message.save()