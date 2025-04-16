import uuid
from django.db import models

from account.models import Account
from land.enums.access_type import ACCESS_ROAD_TYPE
from land.enums.land_status import LAND_STATUS
from land.enums.land_type import LAND_TYPE
from land.enums.zoning_type import ZONING_TYPE
from location.models import Location
from property.enums.rental_duration import RENTAL_DURATION
from user.model.agent import Agent

from django.db.models import Q, QuerySet, OuterRef, Exists, Value, Case, When, IntegerField
from django.core.exceptions import PermissionDenied, ValidationError
from decimal import Decimal
import uuid

class Land(models.Model):
    land_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.RESTRICT, related_name="land")
    category = models.CharField(max_length=100, choices=LAND_TYPE.choices(), default=LAND_TYPE.default())
    land_size = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=32, decimal_places=2)
    rental_duration = models.CharField(max_length=50, choices=RENTAL_DURATION.choices(), null=True, blank=True)
    access_road_type = models.CharField(max_length=100, choices=ACCESS_ROAD_TYPE.choices(), default=ACCESS_ROAD_TYPE.default())
    zoning_type = models.CharField(max_length=100, choices=ZONING_TYPE.choices(), default=ZONING_TYPE.default())
    utilities = models.TextField(null=True, blank=True)
    is_serviced = models.BooleanField(default=False)
    description = models.TextField()
    is_active_account = models.BooleanField(default=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="land")
    listing_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=LAND_STATUS.choices(), default=LAND_STATUS.default)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'land'
        app_label = 'land'

    def __str__(self):
        return f"{self.category} land - {self.land_size} sq meters"

    def delete(self) -> None:
        self.is_deleted = True
        self.save(update_fields=["is_deleted"], skip_validation=True)

    @classmethod
    def soft_delete_land(cls, land_id: uuid.UUID, agent: Agent) -> None:
        land = cls.objects.filter(land_id=land_id, agent=agent).first()
        if land is None:
            raise ValidationError("Ardhi haipo kwenye mfumo wetu")
        land.delete()

    @classmethod
    def save_land(cls, agent: Agent, location: Location, category: str, land_size: Decimal,
                  price: Decimal, description: str, access_road_type: str, zoning_type: str,
                  is_serviced: bool, utilities: str = None, rental_duration: str = None):
        account = Account.get_account(agent=agent)
        if account is None:
            raise PermissionDenied("Hauna akaunti hai ya kuweka ardhi.")
        
        if not account.can_upload(total_property=cls.total_properties_for_agent(agent=agent)):
            raise PermissionDenied("Umefikia kikomo cha mali unazoweza kuweka.")

        instance = cls(
            agent=agent,
            location=location,
            category=category,
            land_size=land_size,
            price=price,
            description=description,
            access_road_type=access_road_type,
            zoning_type=zoning_type,
            is_serviced=is_serviced,
            utilities=utilities,
            rental_duration=rental_duration,
        )

        instance.save()
        return instance

    @classmethod
    def get_land_by_id(cls, land_id: uuid.UUID) -> 'Land':
        return cls.objects.filter(land_id=land_id, is_deleted=False).first()

    @classmethod
    def get_agent_land(cls, agent: Agent, land_id: uuid.UUID) -> 'Land':
        return cls.objects.filter(agent=agent, land_id=land_id, is_deleted=False).first()

    @classmethod
    def get_agent_lands(cls, agent: Agent) -> 'QuerySet[Land]':
        return cls.objects.filter(agent=agent, is_deleted=False).order_by('-listing_date')

    @classmethod
    def land_filter(cls, region: str = None, district: str = None, min_price: Decimal = None, 
                    max_price: Decimal = None, category: str = None, ward: str = None, 
                    street: str = None) -> 'QuerySet[Land]':
        filters = Q(
            status=LAND_STATUS.AVAILABLE.value,
            is_active_account=True,
            is_deleted=False
        )

        if category:
            filters &= Q(category=category)

        if min_price:
            filters &= Q(price__gte=min_price)

        if max_price:
            filters &= Q(price__lte=max_price)

        if region:
            filters &= Q(location__region__iexact=region)

        if district:
            filters &= Q(location__district__iexact=district)

        if ward:
            filters &= Q(location__ward__iexact=ward)

        if street:
            filters &= Q(location__street__iexact=street)

        paid_account_exists = Account.objects.filter(
            agent=OuterRef("agent"),
            is_active=True,
            plan__is_free=False
        ).values("pk")

        queryset = cls.objects.filter(filters).annotate(
            is_paid=Case(
                When(Exists(paid_account_exists), then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            ),
        ).select_related('location').order_by('-is_paid', '-listing_date')

        return queryset

    @classmethod
    def total_properties_for_agent(cls, agent: Agent) -> int:
        return cls.objects.filter(agent=agent, is_deleted=False).count()
