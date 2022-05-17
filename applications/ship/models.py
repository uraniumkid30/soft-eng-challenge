import uuid
from django.db import models
from decimal import Decimal
from applications.generic_app.models import BaseModel


class ShipBaseModel(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    mmsi = models.CharField(max_length=255, blank=True, null=True)
    imo = models.CharField(max_length=255, blank=True, null=True)
    eni = models.CharField(max_length=255, blank=True, null=True)
    country_iso = models.CharField(max_length=255, blank=True, null=True)
    country_name = models.CharField(max_length=255, blank=True, null=True)
    gross_tonnage = models.IntegerField(default=0, blank=True, null=True)
    deadweight = models.IntegerField(default=0, blank=True, null=True)
    length = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, default=Decimal("0.00")
    )
    breadth = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, default=Decimal("0.00")
    )
    year_built = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id} - {self.name} Ship."


class MotherShip(ShipBaseModel):
    @property
    def number_of_ships_owned(self):
        return self.ships.count()

    class Meta:
        verbose_name = "MotherShip - Setting"
        verbose_name_plural = "MotherShip - Settings"


class Ship(ShipBaseModel):
    mother_ship = models.ForeignKey(
        to=MotherShip,
        related_name="ships",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    @property
    def number_of_crew_members_owned(self):
        return self.members.count()

    class Meta:
        verbose_name = "Ship - Setting"
        verbose_name_plural = "Ship - Settings"
