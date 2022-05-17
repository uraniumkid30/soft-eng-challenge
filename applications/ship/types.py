from graphene import relay
from .models import Ship, MotherShip
from graphene_django.types import DjangoObjectType


class ShipType(DjangoObjectType):
    class Meta:
        model = Ship
        exclude = ("id",)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)


class MotherShipType(DjangoObjectType):
    class Meta:
        model = MotherShip
        exclude = ("id",)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
        }
        interfaces = (relay.Node,)
