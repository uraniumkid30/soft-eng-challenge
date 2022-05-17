from typing import Optional
from django.db import transaction
from applications.account.models import User
from applications.generic_app.enums import Roles
from applications.account.selectors import get_user
from applications.generic_app.services import model_update
from applications.generic_app.utils import create_random_word


def user_create(
    *,
    username: str,
    is_active: bool = True,
    password: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    name: Optional[str] = None,
) -> User:
    """Creates User"""
    user = User.objects.create_user(
        username=username,
        is_active=is_active,
        password=password,
        first_name=first_name,
        last_name=last_name,
        name=name,
    )

    return user


@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields = ["first_name", "last_name", "name"]

    user, has_updated = model_update(
        instance=user, fields=non_side_effect_fields, data=data
    )

    return user


def create_collection_of_user_data(number_of_users: int) -> list:
    """Creates a collection of user objects"""
    _names = []
    while len(_names) < number_of_users:
        last_name = create_random_word(10)
        first_name = create_random_word(10)
        username = f"{first_name}{last_name}"
        name = f"{first_name} {last_name}"
        data = {
            "username": username,
            "role": Roles.CREWMEMBER,
            "first_name": first_name,
            "last_name": last_name,
            "name": name,
        }
        user = get_user(**data)
        if user is None:
            data.update({"is_active": True})
            _names.append(User(**data))
    return _names
