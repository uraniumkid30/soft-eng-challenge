import json
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from applications.testsuite.test import GenericTest, MetaTester
from applications.ship.models import Ship, MotherShip
from applications.ship.services import ShipService, MotherShipService
from applications.ship.selectors import MotherShipSelector, ShipSelector
from applications.ship.serializers import MotherShipOutputSerializer


class CreateMothershipTest(GenericTest, metaclass=MetaTester):
    """Test module for inserting a new Mothership"""

    def setUp(self):
        super().setUp()
        self.valid_payload = {
            "name": "Muffin Destroyer",
        }
        self.invalid_payload = {
            "name": "",
        }

    def test_create_valid_mothership(self):
        response = self.client.post(
            reverse("api:Mothership_api:mothership-list"),
            data=json.dumps(self.valid_payload),
            content_type=self.CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_mothership(self):
        response = self.client.post(
            reverse("api:Mothership_api:mothership-list"),
            data=json.dumps(self.invalid_payload),
            content_type=self.CONTENT_TYPE,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetSingleMotherShipTest(GenericTest, metaclass=MetaTester):
    """Test module for GET single Mothership API"""

    def setUp(self):
        super().setUp()
        self.casper = MotherShipService.mothership_create(name="Casper Sails")
        self.muffin = MotherShipService.mothership_create(name="Muffin Destroyer")
        self.rambo = MotherShipService.mothership_create(
            name="Rambo In Her Beauty",
        )
        self.ricky = MotherShipService.mothership_create(
            name="Ricky Swings",
        )

    def test_get_valid_single_mothership(self):
        response = self.client.get(
            reverse(
                "api:Mothership_api:mothership-detail", kwargs={"pk": self.rambo.pk}
            )
        )
        mothership = MotherShipSelector.mothership_get(pk=self.rambo.pk)
        serializer = MotherShipOutputSerializer(mothership)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_mothership(self):
        response = self.client.get(
            reverse("api:Mothership_api:mothership-detail", kwargs={"pk": "30"})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateSingleMotherShipTest(GenericTest, metaclass=MetaTester):
    """Test module for PUT single mothership API"""

    def setUp(self):
        super().setUp()
        self.muffin = MotherShipService.mothership_create(name="Muffin")
        self.valid_payload = {
            "number_of_ships": 1,
        }
        self.invalid_payload = {
            "number_of_ships": 10,
        }

    def test_valid_addition_of_ships_to_mothership(self):
        response = self.client.put(
            reverse(
                "api:Mothership_api:mothership-add-ships", kwargs={"pk": self.muffin.pk}
            ),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_addition_of_ships_to_mothership(self):
        response = self.client.put(
            reverse(
                "api:Mothership_api:mothership-add-ships", kwargs={"pk": self.muffin.pk}
            ),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
