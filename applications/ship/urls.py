from django.conf import settings
from django.urls import include, path
from rest_framework_nested import routers
from .views import MotherShipViewset, ShipViewset


router = routers.SimpleRouter()
router.register(r"motherships", MotherShipViewset)

ships_router = routers.NestedSimpleRouter(router, r"motherships", lookup="motherships")
ships_router.register(r"ships", ShipViewset, basename="ships")

app_name = f"{settings.PROJECT_NAME.capitalize()}_api"

urlpatterns = [
    path("", include(router.urls)),
    path(r"", include(ships_router.urls)),
]
