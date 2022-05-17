from rest_framework import serializers
from applications.ship.models import MotherShip, Ship


class BaseFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)


class MotherShipFilterSerializer(BaseFilterSerializer):
    pass


class ShipFilterSerializer(serializers.Serializer):
    pass


class CrewMemberAdditionFilterSerializer(BaseFilterSerializer):
    pass


class CrewMemberSwithFilterSerializer(BaseFilterSerializer):
    destination_ship_id = serializers.IntegerField(required=False)


class ShipAdditionFilterSerializer(serializers.Serializer):
    number_of_ships = serializers.IntegerField(required=False)


ship_fields = [
    "name",
    "mmsi",
    "imo",
    "eni",
    "country_iso",
    "country_name",
    "gross_tonnage",
]


class MotherShipOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherShip
        fields = ship_fields + ["number_of_ships_owned"]


class ShipOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = ship_fields + ["number_of_crew_members_owned"]
