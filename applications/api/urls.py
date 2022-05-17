from django.urls import path, include
from graphene_django.views import GraphQLView
from applications.api.graphene.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("auth/", include(("applications.authentication.urls", "authentication"))),
    path("users/", include(("applications.account.urls", "users"))),
    path("vessels/", include(("applications.ship.urls", "vessels"))),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
