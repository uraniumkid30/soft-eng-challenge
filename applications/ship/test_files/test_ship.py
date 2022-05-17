import json
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from applications.testsuite.test import GenericTest, MetaTester
from applications.ship.models import Ship, MotherShip
from applications.account.services import user_create
from applications.ship.services import ShipService, MotherShipService
from applications.ship.selectors import MotherShipSelector, ShipSelector
from applications.ship.serializers import (
    ShipOutputSerializer,
)


class GetShipsTest(GenericTest, metaclass=MetaTester):
    """Test module for GET ships list API"""

    def setUp(self):
        super().setUp()
        self.mothership = MotherShipService.mothership_create(name="Destroyer")

    def test_get_valid_ships_list(self):
        response = self.client.get(
            reverse(
                "api:Mothership_api:ships-list",
                kwargs={
                    "motherships_pk": self.mothership.pk,
                },
            )
        )
        mothership_ships = MotherShipSelector.all_mothership_ships_get(
            pk=self.mothership.pk
        )
        serializer = ShipOutputSerializer(mothership_ships, many=True)
        self.assertEqual(len(response.data["results"]), len(serializer.data))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleShipTest(GenericTest, metaclass=MetaTester):
    """Test module for GET single ship from a mothership API"""

    def setUp(self):
        super().setUp()
        self.mothership = MotherShipService.mothership_create(name="Destroyer")
        self.ship = self.mothership.ships.first()

    def test_get_valid_single_ship(self):
        response = self.client.get(
            reverse(
                "api:Mothership_api:ships-detail",
                kwargs={
                    "motherships_pk": self.mothership.pk,
                    "pk": self.ship.pk,
                },
            )
        )
        mothership_ships = MotherShipSelector.all_mothership_ships_get(
            pk=self.mothership.pk
        )
        ship = ShipSelector.ship_get(pk=self.ship.pk, ships=mothership_ships)
        serializer = ShipOutputSerializer(ship)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_motherships_ship(self):
        response = self.client.get(
            reverse(
                "api:Mothership_api:ships-detail",
                kwargs={
                    "motherships_pk": 20,
                    "pk": self.ship.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_invalid_ship(self):
        response = self.client.get(
            reverse(
                "api:Mothership_api:ships-detail",
                kwargs={
                    "motherships_pk": self.mothership.pk,
                    "pk": 30,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleShipTest(GenericTest, metaclass=MetaTester):
    """Test module for PUT single ship API"""

    def setUp(self):
        super().setUp()
        self.mothership = MotherShipService.mothership_create(name="Destroyer")
        self.old_ship = self.mothership.ships.first()
        self.new_ship = self.mothership.ships.last()
        self.old_ship_crew_member = self.old_ship.members.first()
        self.user = user_create(
            first_name="test",
            last_name="tuser",
            username="test_user",
            password="testing",
            name="test user",
        )
        self.valid_addition_payload = {
            "name": "test user",
        }
        self.valid_swap_payload = {
            "name": self.old_ship_crew_member.name,
            "destination_ship_id": self.new_ship.pk,
        }
        self.user.save()

    def test_valid_addition_of_crew_member_to_ship(self):
        response = self.client.put(
            reverse(
                "api:Mothership_api:ships-add-crew-member",
                kwargs={
                    "motherships_pk": self.mothership.pk,
                    "pk": self.old_ship.pk,
                },
            ),
            data=json.dumps(self.valid_addition_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_swapping_of_crew_member_between_ships(self):
        response = self.client.put(
            reverse(
                "api:Mothership_api:ships-swap-user",
                kwargs={
                    "motherships_pk": self.mothership.pk,
                    "pk": self.old_ship.pk,
                },
            ),
            data=json.dumps(self.valid_swap_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteSingleShipTest(GenericTest, metaclass=MetaTester):
    """Test module for deleting an existing ship record"""

    def setUp(self):
        super().setUp()
        self.url = "api:Mothership_api:ships-detail"
        self.mothership = MotherShipService.mothership_create(name="Destroyer")
        self.ship = self.mothership.ships.last()

    def test_valid_delete_ship(self):
        response = self.client.delete(
            reverse(
                self.url,
                kwargs={"motherships_pk": self.mothership.pk, "pk": self.ship.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_ship(self):
        response = self.client.delete(
            reverse(
                self.url,
                kwargs={"motherships_pk": self.mothership.pk, "pk": 30},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_mothership_delete_ship(self):
        response = self.client.delete(
            reverse(
                self.url,
                kwargs={"motherships_pk": 30, "pk": 20},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
