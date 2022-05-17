from django.db.models.query import QuerySet

from applications.account.models import User
from applications.account.filters import UserFilter


def user_get_login_data(*, user: User):
    return {
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }


def user_list(*, filters=None) -> QuerySet[User]:
    filters = filters or {}

    qs = User.objects.all()

    return UserFilter(filters, qs).qs


def get_user(**filters) -> User:
    user = User.objects.filter(**filters)
    return user.first()
