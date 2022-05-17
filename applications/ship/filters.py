import django_filters

from applications.ship.models import Ship, MotherShip


class MotherShipFilter(django_filters.FilterSet):
    class Meta:
        model = MotherShip
        fields = ("name",)


class ShipFilter(django_filters.FilterSet):
    class Meta:
        model = Ship
        fields = ("name",)
