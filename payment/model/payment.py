from decimal import Decimal
import logging
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from account.models import SubscriptionPlan, Account
from payment.enums.payment_status import PaymentStatus
from payment.enums.payment_type import PaymentType
from property.models import Property
from user.models import Agent
from utils.phone_number import validate_phone_number
from django.utils import timezone

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
    payment_date = models.DateTimeField(auto_now_add=True)
    
    is_consumed = models.BooleanField(default=False) 
    consumed_at = models.DateTimeField(null=True, blank=True)

    def mark_as_consumed(self):
        """Mark the payment as consumed and store the timestamp."""
        self.is_consumed = True
        self.consumed_at = timezone.now()
        self.status = PaymentStatus.COMPLETED
        self.save()

    class Meta:
        db_table = 'payment'
        app_label = 'payment'
        
    def __str__(self) -> str:
        return str(self.payment_id)
        
    def activate_account(self) -> None:
        try:
            if not hasattr(self, "_called_from_activate_account"):
                self._called_from_activate_account = True

                account = Account.subscribe(plan=self.plan, agent=self.agent)
                self.mark_as_consumed()

                del self._called_from_activate_account 
            else:
                raise ValueError("Activation already triggered within the same context. Preventing recursion.")
        except ValueError as e:
            raise e
    
    @classmethod
    def auto_mark_property_booked(cls) -> None:
        payments = cls.objects.filter(is_consumed=False)

        if payments:
            for payment in payments:
                if payment.payment_type == PaymentType.BOOKING.value:
                    payment.property.mark_booked()
                    payment.mark_as_consumed()
        
    @classmethod
    def auto_activate_account(cls) -> None:
        payments = cls.objects.filter(is_consumed=False)
        
        if payments:
            logger.info(f"trying to activate account: {[payment for payment in payments]}")
            for payment in payments:
                payment.activate_account()

    @classmethod
    def create(
        cls, phone_number: str, 
        payment_type: PaymentType, 
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
        if payment_type == PaymentType.BOOKING:
            if agent or plan:
                raise ValidationError("For Booking type, agent and plan should not be provided.")
        
        elif payment_type == PaymentType.ACCOUNT:
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

