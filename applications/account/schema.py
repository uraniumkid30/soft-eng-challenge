from graphene import relay, ObjectType
import graphene
from .models import User
from .types import UserType


class UserGrapheneQuery(ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, user_id=graphene.Int())

    def resolve_all_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_user(self, info, user_id):
        return User.objects.get(pk=user_id)
