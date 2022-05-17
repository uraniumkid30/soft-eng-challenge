from graphene import relay, ObjectType
import graphene
from applications.ship.selectors import MotherShipSelector, ShipSelector
from applications.ship.types import ShipType, MotherShipType


class ShipGrapheneQuery(ObjectType):
    all_ships = graphene.List(ShipType, mother_ship=graphene.ID())
    ship = graphene.Field(ShipType, ship_id=graphene.Int())

    def resolve_all_ships(self, info, mother_ship=None, text=None, **kwargs):
        if mother_ship:
            return ShipSelector.ship_list({"mother_ship__id": mother_ship})
        return ShipSelector.ship_list()

    def resolve_ship(self, info, ship_id):
        return ShipSelector.ship_get(pk=ship_id)


class MotherShipGrapheneQuery(ObjectType):
    all_motherships = graphene.List(MotherShipType)
    mothership = graphene.Field(ShipType, mothership_id=graphene.Int())

    def resolve_all_motherships(self, info, **kwargs):
        return MotherShipSelector.mothership_list()

    def resolve_mothership(self, info, mothership_id):
        return MotherShipSelector.mothership_get(pk=mothership_id)
