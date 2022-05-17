from typing import Optional, Iterable

from django.db import transaction

from applications.account.selectors import get_user
from applications.account.services import create_collection_of_user_data
from applications.generic_app.services import model_update
from applications.generic_app.utils import create_random_word
from applications.ship.selectors import MotherShipSelector, ShipSelector
from applications.ship.models import MotherShip, Ship
from applications.account.models import User
from applications.ship.exceptions import (
    MotherShipExceptions,
    ShipExceptions,
    CrewmemberExceptions,
)


class MotherShipService:
    @classmethod
    @transaction.atomic
    def mothership_create(cls, **_fields) -> MotherShip:
        mothership = MotherShip.objects.create(**_fields)
        return mothership

    @classmethod
    def add_ships_to_mother_ship(
        cls,
        mother_ship_id: str,
        number_of_ships_to_add: int = MotherShipSelector.configuration.ship_to_mothership_number,
    ) -> MotherShip:
        _query = {"pk": mother_ship_id}
        mothership = MotherShipSelector.mothership_get(**_query)
        if mothership:
            is_mothership_filled = MotherShipSelector.is_mother_ship_filled_up(
                mothership
            )
            can_mothership_take_more_ships = (
                MotherShipSelector.can_mother_ship_take_more_ships(
                    mothership, number_of_ships_to_add
                )
            )
            if can_mothership_take_more_ships and number_of_ships_to_add:
                ships = ShipService.create_collection_of_ships_data(
                    number_of_ships=number_of_ships_to_add
                )
                mothership = cls.save_ships_to_mothership(mothership, ships)
                return mothership
            else:
                if is_mothership_filled:
                    MotherShipExceptions.ship_number_exceeded(
                        mothership.number_of_ships_owned,
                        number_of_ships_to_add,
                    )
                elif not can_mothership_take_more_ships:
                    MotherShipExceptions.cant_accommodate_more_ships(
                        mothership.number_of_ships_owned,
                        number_of_ships_to_add,
                    )
                MotherShipExceptions.invalid_ship_number(_query)
        MotherShipExceptions.mothership_doesnt_exist(_query)

    @classmethod
    @transaction.atomic
    def save_ships_to_mothership(
        cls,
        mothership: MotherShip,
        ships: Iterable[Ship],
    ) -> MotherShip:
        for _ship in ships:
            mothership.ships.add(_ship, bulk=False)
            mothership.save()
        else:
            return mothership


class ShipService:
    @classmethod
    @transaction.atomic
    def ship_create(cls, **_fields) -> Ship:
        ship = Ship.objects.create(**_fields)
        return ship

    @classmethod
    def ship_create_bulk(
        cls,
        ship_list: list = [],
    ):
        Ship.objects.bulk_create(ship_list)

    @staticmethod
    def create_collection_of_ships_data(number_of_ships: int) -> list:
        _names = []
        while len(_names) < number_of_ships:
            _name = create_random_word()
            ship = ShipSelector.ship_get(filters={"name": _name})
            if ship is None:
                created_ship = Ship(**{"name": _name})
                _names.append(created_ship)
        return _names

    @classmethod
    @transaction.atomic
    def add_crewmember_to_ship(
        cls,
        ship_id: str = "",
        crewmember_name: str = "",
    ) -> Ship:
        ship = ShipSelector.ship_get(pk=ship_id)
        is_ship_filled = ShipSelector.is_ship_filled_up(ship)
        if not is_ship_filled:
            user_query = {"name": crewmember_name}
            user = get_user(**user_query)
            if user:
                ship.members.add(user, bulk=False)
                ship.save()
                return ship
            CrewmemberExceptions.crewmember_doesnt_exist(user_query)
        ShipExceptions.maximum_crewmember_exceeded()

    @classmethod
    @transaction.atomic
    def switch_crewmember_between_ships(
        cls, old_ship_id: str = "", new_ship_id: str = "", crewmember_name: str = ""
    ) -> Ship:
        new_ship = ShipSelector.ship_get(pk=new_ship_id)
        old_ship = ShipSelector.ship_get(pk=old_ship_id)
        if new_ship and old_ship:
            is_ship_filled = ShipSelector.is_ship_filled_up(new_ship)
            if not is_ship_filled:
                user_query = {"name": crewmember_name}
                user = get_user(**user_query)
                if user:
                    old_ship.members.remove(user)
                    new_ship.members.add(user, bulk=False)
                    new_ship.save()
                    old_ship.save()
                    return {"new_ship": new_ship, "old_ship": old_ship}
                CrewmemberExceptions.crewmember_doesnt_exist(user_query)
            ShipExceptions.maximum_crewmember_exceeded()

    @classmethod
    def add_crewmembers_to_ship(
        cls,
        ship_id: int,
    ) -> MotherShip:
        ship = ShipSelector.ship_get(pk=ship_id)
        if ship:
            is_ship_filled = ShipSelector.is_ship_filled_up(ship)
            if not is_ship_filled:
                number_of_crew_members_to_create = (
                    ShipSelector.configuration.crewmember_to_ship_number
                )
                crew_members = create_collection_of_user_data(
                    number_of_users=number_of_crew_members_to_create
                )
                ship = cls.save_crewmembers_to_ship(ship, crew_members)
                return ship
            ShipExceptions.maximum_crewmember_exceeded()

    @classmethod
    @transaction.atomic
    def save_crewmembers_to_ship(
        cls,
        ship: Ship,
        crew_members: Iterable[User],
    ) -> MotherShip:
        for crew_member in crew_members:
            ship.members.add(crew_member, bulk=False)
            ship.save()
        else:
            return ship
