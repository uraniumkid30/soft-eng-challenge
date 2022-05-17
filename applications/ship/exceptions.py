from django.core.exceptions import (
    ValidationError,
    ObjectDoesNotExist,
    EmptyResultSet,
)


class CustomExceptions:
    @classmethod
    def _raise_validation_error(cls, custom_message):
        raise ValidationError(custom_message)

    @classmethod
    def _raise_non_existent_object_error(cls, custom_message):
        raise ObjectDoesNotExist(custom_message)

    @classmethod
    def _raise_empty_result_error(cls, custom_message):
        raise ObjectDoesNotExist(custom_message)


class MotherShipExceptions(CustomExceptions):
    @classmethod
    def ship_number_exceeded(cls, current_ship_count, number_of_ships_to_add):
        message = f"Mothership contains {current_ship_count} ships already."
        message += f"adding {number_of_ships_to_add} will exceed the limit"
        cls._raise_validation_error(message)

    @classmethod
    def cant_accommodate_more_ships(cls, current_ship_count, number_of_ships_to_add):
        cls.ship_number_exceeded(current_ship_count, number_of_ships_to_add)

    @classmethod
    def invalid_ship_number(cls, number_of_ships_to_add):
        message = f"You asked me to add an invalid number of ships ({number_of_ships_to_add}) to Mothership"
        cls._raise_validation_error(message)

    @classmethod
    def mothership_doesnt_exist(cls, query_data):
        message = f"Mothership with data {query_data} doesnt exist"
        cls._raise_validation_error(message)


class ShipExceptions(CustomExceptions):
    @classmethod
    def maximum_crewmember_exceeded(cls, current_crewmember_count):
        message = f"Ship contains {current_crewmember_count} ships already."
        message += f"adding an extra crewmember will exceed the limit"
        cls._raise_validation_error(message)

    @classmethod
    def invalid_crewmember_number(cls, crewmember_name):
        message = f"You asked me to add an invalid number of crewmember ({crewmember_name}) to Ship"
        cls._raise_validation_error(message)

    @classmethod
    def ship_doesnt_exist(cls, query_data):
        message = f"Ship with data {query_data} doesnt exist"
        cls._raise_validation_error(message)


class CrewmemberExceptions(CustomExceptions):
    @classmethod
    def crewmember_doesnt_exist(cls, query_data):
        message = f"Crewmember with data {query_data} doesnt exist"
        cls._raise_validation_error(message)
