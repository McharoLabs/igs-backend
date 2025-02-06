from decimal import Decimal
import logging
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from account.models import Account
from booking.models import Booking
from payment.enums.payment_status import PaymentStatus
from payment.enums.payment_type import PaymentType
from property.models import Property
from subscription_plan.models import SubscriptionPlan
from user.models import Agent
from utils.phone_number import validate_phone_number
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

logger = logging.getLogger(__name__)

class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    
    agent = models.ForeignKey(Agent, on_delete=models.RESTRICT, related_name="payments", null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.RESTRICT, related_name="payment", null=True, blank=True)
    
    property = models.ForeignKey(Property, on_delete=models.RESTRICT, related_name="payments", null=True, blank=True)
    
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number], null=False)
    status = models.CharField(max_length=50, choices=PaymentStatus.choices(), default=PaymentStatus.default())
    payment_type = models.CharField(max_length=100, choices=PaymentType.choices(), default=PaymentType.default())
    order_id = models.CharField(max_length=255, null=True)
    message = models.CharField(max_length=255, null=True)
    payment_status = models.CharField(null=True, max_length=100)
    reference = models.CharField(null=True, max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    is_consumed = models.BooleanField(default=False) 
    consumed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'payment'
        app_label = 'payment'

    def mark_as_consumed(self):
        """Mark the payment as consumed and store the timestamp."""
        self.is_consumed = True
        self.consumed_at = timezone.now()
        self.status = PaymentStatus.COMPLETED.value
        self.save()

        
    def __str__(self) -> str:
        return str(self.payment_id)
    
    @classmethod
    def delete_pending_payments(cls):
        """Delete pending payments that have stayed for 1 day."""
        one_day_ago = timezone.now() - timedelta(days=1)
        
        pending_payments = cls.objects.filter(status=PaymentStatus.PENDING.value, payment_date__lt=one_day_ago)
        
        deleted_count, _ = pending_payments.delete()
        
        logger.info(f"{deleted_count} pending payments older than 1 day were deleted.")
        
    
    def update_order_and_message(self, order_id: str, message: str) -> None:
        """Update payment by inserting order id and message from the payment gateway after initializing the request

        Args:
            order_id (str): Order ID from the payment gateway
            message (str): Message from the payment gateway
        """
        self.order_id = order_id
        self.message = message
        self.save(update_fields=['order_id', 'message'])
        
    def on_complete_payment(self, *, payment_status: str, reference: str, customer_name: str = None, customer_email: str = None) -> None:
        """Update payment by inserting payment status and reference from the payment gateway on webhook call

        Args:
            payment_status (str): Payment status from the payment gateway
            reference (str): Payment reference from the payment gateway
        """
        self.payment_status = payment_status
        self.reference = reference
        
        with transaction.atomic():
            if payment_status.upper() == 'COMPLETED':
                if self.agent is None:
                    self.property.mark_booked()
                    self.mark_as_consumed()
                    Booking.save_booking(
                            property=self.property, 
                            customer_name=customer_name, 
                            customer_email=customer_email, 
                            customer_phone_number=self.phone_number
                        )
                elif self.agent:
                    try:
                        Account.subscribe(plan=self.plan, agent=self.agent)
                        self.mark_as_consumed()
                    except ValueError as e:
                        logger.error(f"An error occured: {e}", exc_info=True)
                        raise e
                
            self.save(update_fields=['reference', 'payment_status'])
            
    @classmethod
    def get_payment_for_callback(cls, payment_id: uuid.UUID, order_id: str) -> 'Payment | None':
        """Retrieve payment for the webhook

        Args:
            payment_id (uuid.UUID): Payment ID to filter the payment instance
            order_id (str): Order ID from initiated payment for filtering the payment instance

        Returns:
            Payment | None: Payment instance if found, otherwise None
        """
        return cls.objects.filter(payment_id=payment_id, order_id=order_id).first()

    @classmethod
    def create(
        cls, phone_number: str, 
        payment_type: str, 
        amount: Decimal, 
        agent: Agent = None,
        property: Property = None,
        plan: SubscriptionPlan = None
    ) -> 'Payment':
        """Class method to create and save a temporary payment.

        This method validates the payment data and ensures that the provided
        information is consistent with the payment type. It will raise a 
        ValidationError if there are any inconsistencies in the payment data.

        Args:
            phone_number (str): Tenant or agent phone number. This is required 
                                for identifying the user associated with the payment.
            payment_type (PaymentType): The type of payment being made (e.g., 
                                        booking, account, etc.).
            amount (Decimal): The amount paid. This should be a valid decimal 
                            value representing the payment sum.
            agent (Agent, optional): An optional agent instance associated 
                                    with the payment. Default is None.
            property (Property, optional): An optional property instance 
                                        associated with the payment. 
                                        Default is None.
            plan (SubscriptionPlan, optional): An optional subscription plan 
                                            instance linked to the payment. 
                                            Default is None.

        Raises:
            ValidationError: If the payment type and provided data are inconsistent, 
                            a ValidationError will be raised.
            ValueError: If the provided amount is not a valid decimal number.

        Returns:
            Payment: The created Payment instance that has been validated and saved.
        """
        if payment_type == PaymentType.BOOKING.value:
            if agent or plan:
                raise ValidationError("For Booking type, agent and plan should not be provided.")
        
        elif payment_type == PaymentType.ACCOUNT.value:
            if property:
                raise ValidationError("For Account type, property should not be provided.")
        
        try:
            amount = Decimal(amount)
        except:
            raise ValueError("Invalid amount, it should be a decimal.")

        payment = cls(
            amount=amount,
            agent=agent,
            property=property,
            plan=plan,
            phone_number=phone_number,
            payment_type=payment_type
        )
        
        payment.save()
        
        return payment

