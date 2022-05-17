from graphene_django.types import DjangoObjectType
from .models import User
from graphene import relay


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ("password",)
        # Allow for some more advanced filtering here
        filter_fields = {
            "first_name": ["exact", "icontains", "istartswith"],
            "last_name": ["exact", "icontains"],
            "role": ["exact"],
        }
        interfaces = (relay.Node,)
