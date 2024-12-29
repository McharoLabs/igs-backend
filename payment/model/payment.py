from decimal import Decimal
import logging
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from account.models import SubscriptionPlan, Account
from house.models import House, Room
from payment.enums.payment_status import PaymentStatus
from payment.enums.payment_type import PaymentType
from user.models import Agent, LandLord
from utils.phone_number import validate_phone_number
from django.utils import timezone

logger = logging.getLogger(__name__)

class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    
    # Fields for booking type
    agent = models.ForeignKey(Agent, on_delete=models.RESTRICT, related_name="agent_account_payment", null=True, blank=True)
    landlord = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="landlord_account_payment", null=True, blank=True)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.RESTRICT, related_name="plan_payment", null=True, blank=True)
    
    # Fields for account type
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_name="house_payment", null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.RESTRICT, related_name="room_payment", null=True, blank=True)
    
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number], null=False)
    status = models.CharField(max_length=50, choices=PaymentStatus.choices(), default=PaymentStatus.default())
    payment_type = models.CharField(max_length=100, choices=PaymentType.choices(), default=PaymentType.default())
    payment_date = models.DateTimeField(auto_now_add=True)
    
    # Fields to track payment consumption
    is_consumed = models.BooleanField(default=False) 
    consumed_at = models.DateTimeField(null=True, blank=True)

    def mark_as_consumed(self):
        """Mark the payment as consumed and store the timestamp."""
        self.is_consumed = True
        self.consumed_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'payment'
        
    def __str__(self) -> str:
        return str(self.payment_id)
        
    def activate_account(self) -> None:
        try:
            if not hasattr(self, "_called_from_activate_account"):
                self._called_from_activate_account = True

                account = Account.subscribe(plan=self.plan, agent=self.agent, landlord=self.landlord)
                self.mark_as_consumed()

                del self._called_from_activate_account 
            else:
                raise ValueError("Activation already triggered within the same context. Preventing recursion.")
        except ValueError as e:
            raise e
    
    @classmethod
    def auto_mark_room_booked(cls) -> None:
        payments = cls.objects.filter(is_consumed=False)

        if payments:
            for payment in payments:
                if payment.house: 
                    if payment.house.is_full_house_rental:
                        payment.house.mark_booked()
                        payment.mark_as_consumed()
                        logger.info(f"House {payment.house} marked booked")
                    elif payment.room:
                        payment.room.mark_booked()
                        payment.mark_as_consumed()
                        logger.info(f"Room {payment.room} marked booked")
        
    @classmethod
    def auto_activate_account(cls) -> None:
        payments = cls.objects.filter(is_consumed=False)
        
        if payments:
            logger.info(f"trying to activate account: {[payment for payment in payments]}")
            for payment in payments:
                payment.activate_account()

    @classmethod
    def create_payment(
        cls, phone_number: str, 
        payment_type: PaymentType, 
        amount: Decimal, 
        agent: Agent = None, 
        landlord: LandLord = None, 
        house: House = None, 
        room: Room = None, 
        plan: SubscriptionPlan = None
    ) -> 'Payment':
        """Creates a payment instance based on payment_type and the provided parameters.
        
        Args:
            phone_number (str): Phone number for the request
            payment_type (PaymentType): The type of the payment (Booking or Account).
            amount (Decimal): The amount of the payment.
            agent (Agent, optional): The agent associated with the payment (if payment_type is BOOKING).
            landlord (LandLord, optional): The landlord associated with the payment (if payment_type is BOOKING).
            house (House, optional): The house associated with the payment (if payment_type is ACCOUNT).
            room (Room, optional): The room associated with the payment (if payment_type is ACCOUNT).
            plan (SubscriptionPlan, optional): The subscription plan associated with the payment (if payment_type is BOOKING).
        
        Raises:
            ValidationError: If both agent and landlord are provided for booking type.
            ValueError: If the amount is not a valid decimal.
        
        Returns:
            Payment: The created Payment instance.
        """
        
        if payment_type == PaymentType.BOOKING:
            if agent or landlord or plan:
                raise ValidationError("For Booking type, agent, landlord, and plan should not be provided.")
            
        elif payment_type == PaymentType.ACCOUNT:
            if house or room:
                raise ValidationError("For Account type, house and room should not be provided.")
            
        try:
            amount = Decimal(amount)
        except:
            raise ValueError("Invalid amount, it should be a decimal.")

        payment = cls(
            amount=amount,
            agent=agent,
            landlord=landlord,
            house=house,
            room=room,
            plan=plan,
            phone_number=phone_number,
            payment_type=payment_type
        )
        payment.save()
        return payment
