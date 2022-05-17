from django.apps import AppConfig


class ShipConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "applications.ship"

    def ready(self):
        try:
            import applications.ship.signals
        except:
            pass
