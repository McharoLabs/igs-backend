import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta

from account.models import SubscriptionPlan
from user.models import Agent, LandLord
from django.db.models import QuerySet

class Account(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, related_name="agent_account")
    landlord = models.ForeignKey(LandLord, on_delete=models.SET_NULL, null=True, related_name="landlord_account")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            if hasattr(self.plan, 'duration_days'):
                self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        owner = self.account_owner()
        plan_name = self.plan.name if self.plan else 'No Plan'
        return f"Account for {owner} ({plan_name})"
    
    def expire_account(self) -> None:
        """
        Expires the account by setting `is_active` to False, only if the account is still active 
        and the `end_date` is in the future.
        """
        if self.is_active and self.end_date > timezone.now():
            self.is_active = False
            self.save()

    
    def account_owner(self) -> str:
        """Returns the full name of the account owner (either agent or landlord)."""
        if self.agent:
            return f"{self.agent.first_name} {self.agent.middle_name} {self.agent.last_name}"
        if self.landlord:
            return f"{self.landlord.first_name} {self.landlord.middle_name} {self.landlord.last_name}"
        
    def can_upload_house(self, total_house: int) -> bool:
        """
        Checks if the agent or landlord associated with this account can upload another house.
        This is based on the account being active and the account's subscription plan allowing the upload 
        of the specified number of houses.

        Args:
            total_house (int): The total number of houses the agent or landlord has already uploaded.

        Returns:
            bool: Returns True if the account is active and the number of uploaded houses is within the limit
                specified by the account's subscription plan. Returns False otherwise.
        """
        if self.is_active and self.plan and total_house < self.plan.max_houses:
            return True
        
        return False

    @classmethod
    def get_account(cls, agent: Agent = None, landlord: LandLord = None) -> 'Account':
        """
        Retrieve the active account associated with either an agent or a landlord. This method ensures that 
        only one of the two parameters (agent or landlord) is provided. If both are provided, 
        a ValueError will be raised. If neither is provided, a ValueError will also be raised.

        Args:
            agent (Agent, optional): The agent whose account is to be retrieved. Defaults to None.
            landlord (LandLord, optional): The landlord whose account is to be retrieved. Defaults to None.

        Raises:
            ValueError: If both `agent` and `landlord` are provided, or if neither is provided.

        Returns:
            Account: The active `Account` associated with the given agent or landlord. If no active account 
            is found, the method returns `None`.
        """
        if agent and landlord:
            raise ValueError("Cannot provide both agent and landlord.")
        
        if agent:
            return cls.objects.filter(agent=agent, is_active=True).first()
        
        if landlord:
            return cls.objects.filter(landlord=landlord, is_active=True).first()
        
        raise ValueError("Must provide either an agent or a landlord.")
    
    @classmethod
    def get_active_accounts(cls) -> 'QuerySet[Account]':
        """Retrieve all active accounts

        Returns:
            QuerySet[Account]: QuerySet of active account objects if found, otherwise None
        """
        return cls.objects.filter(is_active=True)
    
    @classmethod
    def get_inactive_accounts(cls) -> 'QuerySet[Account]':
        """Retrieve all inactive accounts

        Returns:
            QuerySet[Account]: QuerySet of inactive account objects if found, otherwise None
        """
        return cls.objects.filter(is_active=False)