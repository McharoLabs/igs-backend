import uuid
from django.db import models
from django.db.models import QuerySet
import logging

from user.model.agent import Agent

logger = logging.getLogger(__name__)

class SubscriptionPlan(models.Model):
    subscription_plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, help_text="e.g., 'Basic', 'Premium'")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_houses = models.IntegerField()
    duration_days = models.IntegerField(default=30)
    is_visible = models.BooleanField(default=True, help_text="Whether this plan should be displayed to users.")
    is_free = models.BooleanField(default=False, help_text="Indicates whether the plan is free.")

    class Meta:
        db_table = 'subscription_plan'
        app_label = 'subscription_plan'

    def __str__(self):
        return f"{self.name} - ${self.price} (Max {self.max_houses} Houses)"
    
    @classmethod
    def get_free_plan(cls) -> 'SubscriptionPlan':
        return cls.objects.filter(is_free=True).first()
    
    @classmethod
    def get_plan_by_id(cls, subscription_plan_id: uuid.UUID) -> 'SubscriptionPlan':
        """Retrieve plan by subscription plan id

        Args:
            subscription_plan_id (uuid.UUID): Subscription plan id to find the plan

        Returns:
            SubscriptionPlan: Subscription plan instance if found, otherwise None
        """
        return cls.objects.filter(subscription_plan_id=subscription_plan_id).first()

    @classmethod
    def get_all_plans(cls) -> QuerySet['SubscriptionPlan']:
        """
        Retrieves all subscription plans from the database.

        Returns:
            QuerySet['SubscriptionPlan']: A queryset containing all SubscriptionPlan objects.
        """
        return cls.objects.filter(is_visible=True, is_free=False)