from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MotherShip, Ship
from .services import ShipService, MotherShipService


@receiver(post_save, sender=MotherShip)
def create_mother_ship(sender, instance, created, **kwargs):
    if created:
        MotherShipService.add_ships_to_mother_ship(
            mother_ship_id=instance.pk,
        )


@receiver(post_save, sender=Ship)
def create_ship(sender, instance, created, **kwargs):
    if created:
        ShipService.add_crewmembers_to_ship(ship_id=instance.pk)
