import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db.models import QuerySet
from django.db import transaction
import logging

from subscription_plan.models import SubscriptionPlan
from user.model.agent import Agent

logger = logging.getLogger(__name__)

class Account(models.Model):
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True, related_name="agent_account")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'account'
        app_label = 'account'

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            if hasattr(self.plan, 'duration_days'):
                self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        owner = self.account_owner()
        plan_name = self.plan.name if self.plan else 'No Plan'
        return f"Account for {owner} ({plan_name})"
    
    def expire_account(self) -> bool:
        """
        Expires the account by setting `is_active` to False, only if the account is still active 
        and the `end_date` is in the future.
        """
        if self.is_active:
            if self.end_date <= timezone.now():
                self.is_active = False
                self.save(update_fields=['is_active'])
                logger.info(f"Account {self.account_id} expired and deactivated.")
                return True
            return False
        return False

    def account_owner(self) -> str:
        """Returns the full name of the account owner (agent)"""
        if self.agent:
            return f"{self.agent.first_name} {self.agent.middle_name} {self.agent.last_name}"
        
    def can_upload(self, total_property: int) -> bool:
        """
        Checks if the agent associated with this account can upload another house.
        This is based on the account being active and the account's subscription plan allowing the upload 
        of the specified number of houses.

        Args:
            total_property (int): The total number of houses the agent has already uploaded.

        Returns:
            bool: Returns True if the account is active and the number of uploaded houses is within the limit
                specified by the account's subscription plan. Returns False otherwise.
        """
        if self.is_active and self.plan and total_property < self.plan.max_houses:
            return True
        
        return False
    
    @classmethod
    def subscribe(cls, plan: SubscriptionPlan, agent: Agent) -> None:
        """Subscribe the plan and create a new account for the agent and deactivate the previous active account if found

        Args:
            plan (SubscriptionPlan): Subscription plan instance for the agent
            agent (Agent): Agent for the subscribed account.

        Returns:
            str: Success message for created account
        """
        
        with transaction.atomic():
            current_active_account = cls.objects.filter(agent=agent, is_active=True).first()

            if current_active_account:
                current_active_account.is_active = False
                current_active_account.save()

            account = cls(
                agent=agent,
                plan=plan
            )

            account.save()

            logger.info(f"Plan subscription for {agent}")
            
    @classmethod
    def subscribe_free_account(cls, plan: SubscriptionPlan, agent: Agent) -> None:
        with transaction.atomic():
            current_active_account = cls.objects.filter(agent=agent, is_active=True).first()

            if current_active_account:
                return None

            account = cls(
                agent=agent,
                plan=plan
            )

            account.save()

            logger.info(f"Plan subscription for {agent}")
            
    def get_agents_without_account() -> 'QuerySet[Agent]':
        return Agent.objects.filter(agent_account__isnull=True)
        

    @classmethod
    def get_account(cls, agent: Agent):
        """
        Retrieve the active account associated with either an agent. This method ensures that 
        only one of the two parameters (agent) is provided. If both are provided, 
        a ValueError will be raised. If neither is provided, a ValueError will also be raised.

        Args:
            agent (Agent): The agent whose account is to be retrieved. Defaults to None.

        Returns:
            Account: The active `Account` associated with the given agent. If no active account 
            is found, the method returns `None`.
        """
        
        return cls.objects.filter(agent=agent, is_active=True).first()
    
    @classmethod
    def get_active_accounts(cls) -> 'QuerySet[Account]':
        """Retrieve all active accounts

        Returns:
            QuerySet[Account]: QuerySet of active account objects if found, otherwise None
        """
        return cls.objects.filter(is_active=True)
    
    @classmethod
    def get_inactive_accounts(cls) -> QuerySet['Account']:
        """Retrieve all inactive accounts deactivated within the last 7 days.

        Returns:
            QuerySet[Account]: QuerySet of inactive account objects if found, otherwise an empty queryset.
        """
        seven_days_ago = timezone.now() - timedelta(days=7)
        return cls.objects.filter(is_active=False, end_date__gte=seven_days_ago)
