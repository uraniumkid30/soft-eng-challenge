from django.db import models
from django.conf import settings
from applications.generic_app.models import BaseModel


class BaseConfiguration(BaseModel):
    maximum_ship_number = models.IntegerField(blank=True, null=True)
    ship_to_mothership_number = models.IntegerField(blank=True, null=True)
    maximum_crewmember_number = models.IntegerField(blank=True, null=True)
    crewmember_to_ship_number = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = "BaseConfigration - Setting"
        verbose_name_plural = "BaseConfigration - Settings"

    def __str__(self):
        return f"{self.id} - {self.name}'s BaseConfigration."

    def save(self):
        if not self.has_row_items():
            super(BaseConfiguration, self).save()

    def has_row_items(self) -> bool:
        return BaseConfiguration.objects.exists()


class BusinessConfiguration:
    def __init__(
        self,
    ):
        self.is_model_configuration_available = BaseConfiguration.objects.exists()

    @property
    def base_configuration(self):
        if self.is_model_configuration_available:
            return BaseConfiguration.objects.all().first()

    @property
    def maximum_ship_number(self):
        if self.is_model_configuration_available:
            return self.base_configuration.maximum_ship_number
        return settings.MAXIMUM_SHIP_NUMBER

    @property
    def ship_to_mothership_number(self):
        if self.is_model_configuration_available:
            return self.base_configuration.ship_to_mothership_number
        return settings.SHIP_TO_MOTHERSHIP_NUMBER

    @property
    def maximum_crewmember_number(self):
        if self.is_model_configuration_available:
            return self.base_configuration.maximum_crewmember_number
        return settings.MAXIMUM_CREWMEMBER_NUMBER

    @property
    def crewmember_to_ship_number(self):
        if self.is_model_configuration_available:
            return self.base_configuration.crewmember_to_ship_number
        return settings.CREWMEMBER_TO_SHIP_NUMBER
