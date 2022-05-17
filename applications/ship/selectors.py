from django.db.models import Q, F
from typing import Iterable
from django.db.models.query import QuerySet
from applications.account.models import User
from applications.ship.models import MotherShip, Ship
from applications.ship.filters import MotherShipFilter, ShipFilter
from applications.configuration.models import BusinessConfiguration


class MotherShipSelector:
    configuration: BusinessConfiguration = BusinessConfiguration()

    @classmethod
    def is_mother_ship_filled_up(cls, mothership: MotherShip) -> bool:
        maximum_ship_to_mothership_capacity = mothership.number_of_ships_owned
        return (
            maximum_ship_to_mothership_capacity
            >= cls.configuration.maximum_ship_to_mothership_capacity
        )

    @classmethod
    def can_mother_ship_take_more_ships(
        cls, mothership: MotherShip, ship_number: int
    ) -> bool:
        remaining_capacity = (
            cls.configuration.maximum_ship_to_mothership_capacity
            - mothership.number_of_ships_owned
        )
        return remaining_capacity >= ship_number

    @classmethod
    def mothership_list(cls, *, filters=None) -> QuerySet[MotherShip]:
        filters = filters or {}

        qs = MotherShip.objects.all()

        return MotherShipFilter(filters, qs).qs

    @classmethod
    def mothership_get(cls, *, filters=None, pk=None) -> MotherShip:
        filters = filters or {}
        qs = MotherShip.objects.filter(pk=pk)
        return MotherShipFilter(filters, qs).qs.first()

    @classmethod
    def all_mothership_ships_get(cls, *, filters=None, pk=None) -> QuerySet[Ship]:
        mothership = cls.mothership_get(filters=filters, pk=pk)
        if mothership is None:
            return mothership
        return mothership.ships


class ShipSelector:
    configuration: BusinessConfiguration = BusinessConfiguration()

    @classmethod
    def is_ship_filled_up(cls, ship: Ship) -> bool:
        maximum_crewmember_to_ship_capacity = ship.number_of_crew_members_owned
        return (
            maximum_crewmember_to_ship_capacity
            >= cls.configuration.maximum_crewmember_to_ship_capacity
        )

    @classmethod
    def can_ship_take_more_crewmembers(
        cls, ship: Ship, number_of_crewmembers: int
    ) -> bool:
        remaining_capacity = (
            cls.configuration.maximum_crewmember_to_ship_capacity
            - ship.number_of_crew_members_owned
        )
        return remaining_capacity >= number_of_crewmembers

    @classmethod
    def ship_list(
        cls, *, filters=None, pk: int = None, ships: QuerySet[Ship] = None
    ) -> QuerySet[Ship]:
        if ships is None:
            ships = Ship.objects.all()
        filters = filters or {}

        return ShipFilter(filters, ships).qs

    @classmethod
    def ship_get(cls, *, filters=None, pk=None, ships: QuerySet[Ship] = None) -> Ship:
        if ships is None:
            ships = Ship.objects
        filters = filters or {}
        qs = ships.filter(pk=pk)
        return ShipFilter(filters, qs).qs.first()

    @classmethod
    def all_ships_crewmembers_get(cls, *, filters=None, pk=None) -> QuerySet[User]:
        ship = cls.ship_get(filters=filters, pk=pk)
        if ship is None:
            return ship
        return ship.members
