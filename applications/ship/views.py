from django.shortcuts import render
from rest_framework import status, viewsets

from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .serializers import (
    MotherShipFilterSerializer,
    MotherShipOutputSerializer,
    ShipAdditionFilterSerializer,
    ShipFilterSerializer,
    ShipOutputSerializer,
    CrewMemberSwithFilterSerializer,
    CrewMemberAdditionFilterSerializer,
)
from .selectors import MotherShipSelector, ShipSelector
from .services import MotherShipService, ShipService
from applications.ship.models import Ship, MotherShip
from applications.api.pagination import CustomPaginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class MotherShipViewset(viewsets.ViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = MotherShip.objects.all()
    serializer_class = MotherShipOutputSerializer

    @method_decorator(login_required)
    def list(self, request, *args, **kwargs):
        input_ser = MotherShipFilterSerializer(data=request.query_params)
        input_ser.is_valid(raise_exception=True)
        motherships = MotherShipSelector.mothership_list(
            filters=input_ser.validated_data
        )
        payload = {
            "request": request,
            "query_set": motherships,
            "serializer": MotherShipOutputSerializer,
        }
        paginator_response = CustomPaginator(**payload)
        return paginator_response.data

    def retrieve(self, request, pk=None, *args, **kwargs):
        mothership = MotherShipSelector.mothership_get(pk=pk)
        if mothership is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response_payload = MotherShipOutputSerializer(mothership)
        return Response(response_payload.data)

    def create(self, request, *args, **kwargs):
        input_ser = MotherShipFilterSerializer(data=request.data)
        input_ser.is_valid(raise_exception=True)
        mothership = MotherShipService.mothership_create(**input_ser.validated_data)
        response_payload = MotherShipOutputSerializer(mothership)
        return Response(response_payload.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        input_ser = MotherShipFilterSerializer(data=request.query_params)
        input_ser.is_valid(raise_exception=True)
        mothership = MotherShipSelector.mothership_get(pk=pk)
        if mothership is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        mothership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["put"])
    def add_ships(self, request, pk=None, *args, **kwargs):
        input_ser = ShipAdditionFilterSerializer(data=request.data)
        input_ser.is_valid(raise_exception=True)
        mothership = MotherShipSelector.mothership_get(pk=pk)
        if mothership is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        number_of_ships = input_ser.validated_data["number_of_ships"]
        mothership = MotherShipService.add_ships_to_mother_ship(pk, number_of_ships)
        return Response(
            {"result": f"Successfully Added {number_of_ships} ship {mothership.name}"}
        )


class ShipViewset(viewsets.ViewSet):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Ship.objects.all()
    serializer_class = ShipOutputSerializer

    def list(self, request, *args, **kwargs):
        input_ser = ShipFilterSerializer(data=request.query_params)
        input_ser.is_valid(raise_exception=True)
        mother_ship_pk = kwargs.get("motherships_pk")
        mothership_ships = MotherShipSelector.all_mothership_ships_get(
            pk=mother_ship_pk
        )
        ships = ShipSelector.ship_list(
            filters=input_ser.validated_data, ships=mothership_ships
        )
        payload = {
            "request": request,
            "query_set": ships,
            "serializer": ShipOutputSerializer,
        }
        paginator_response = CustomPaginator(**payload)
        return paginator_response.data

    def retrieve(self, request, pk=None, *args, **kwargs):
        mother_ship_pk = kwargs.get("motherships_pk")
        mothership_ships = MotherShipSelector.all_mothership_ships_get(
            pk=mother_ship_pk
        )
        if mothership_ships is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ship = ShipSelector.ship_get(pk=pk, ships=mothership_ships)
        if ship is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response_payload = ShipOutputSerializer(ship)
        return Response(response_payload.data)

    @action(detail=True, methods=["put"])
    def swap_user(self, request, pk=None, *args, **kwargs):
        input_ser = CrewMemberSwithFilterSerializer(data=request.data)
        input_ser.is_valid(raise_exception=True)
        new_ship_pk = input_ser.validated_data["destination_ship_id"]
        crew_member_name = input_ser.validated_data["name"]
        ships = ShipService.switch_crewmember_between_ships(
            old_ship_id=pk,
            new_ship_id=new_ship_pk,
            crewmember_name=crew_member_name,
        )
        new_ship = ships.get("new_ship")
        old_ship = ships.get("old_ship")
        return Response(
            {
                "result": f"Successfully Switched crew member {crew_member_name} from {old_ship.name} to {new_ship.name} ship."
            }
        )

    @action(detail=True, methods=["put"])
    def add_crew_member(self, request, pk=None, *args, **kwargs):
        input_ser = CrewMemberAdditionFilterSerializer(data=request.data)
        input_ser.is_valid(raise_exception=True)
        crew_member_name = input_ser.validated_data["name"]
        ship = ShipService.add_crewmember_to_ship(
            pk,
            crew_member_name,
        )
        return Response(
            {
                "result": f"Successfully Added crew member {crew_member_name} to ship {ship.name}"
            }
        )

    def destroy(self, request, pk=None, *args, **kwargs):
        mother_ship_pk = kwargs.get("motherships_pk")
        mothership_ships = MotherShipSelector.all_mothership_ships_get(
            pk=mother_ship_pk
        )
        if mothership_ships is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ship = ShipSelector.ship_get(pk=pk, ships=mothership_ships)
        if ship is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ship.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
