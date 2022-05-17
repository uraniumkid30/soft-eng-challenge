from django.contrib import admin
from .models import Ship, MotherShip
from django_object_actions import DjangoObjectActions


@admin.register(Ship)
class ShipAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = (
        "name",
        "number_of_crew_members_owned",
    )

    def number_of_crew_members_owned(self, obj):
        try:
            res = obj.number_of_crew_members_owned
        except Exception as err:
            res = " - "
        return res

    number_of_crew_members_owned.short_description = "Crew Memebers owned"


@admin.register(MotherShip)
class MotherShipAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = (
        "name",
        "number_of_ships_owned",
    )

    def number_of_ships_owned(self, obj):
        try:
            number_of_ships_owned = obj.number_of_ships_owned
        except:
            number_of_ships_owned = " - "
        return number_of_ships_owned

    number_of_ships_owned.short_description = "Ships Owned"
