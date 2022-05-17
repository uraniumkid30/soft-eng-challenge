from django.db import models
from applications.ship.models import Ship

import uuid
from applications.generic_app.enums import Roles
from django.contrib.auth.models import (
    BaseUserManager as BUM,
    AbstractUser,
)


class BaseUserManager(BUM):
    def create_user(
        self,
        username: str,
        is_active: bool = True,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        name: str = None,
    ):
        if not username:
            raise ValueError("Users must have an email address")

        user: User = self.model(
            username=username,
            is_active=is_active,
            role=Roles.CREWMEMBER,
        )
        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if name:
            user.name = name

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.is_superuser = False
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        username: str,
        password: str = None,
        first_name: str = None,
        last_name: str = None,
        name: str = None,
    ):
        user: User = self.create_user(
            username=username,
            is_active=True,
            password=password,
        )
        if first_name:
            user.first_name = first_name

        if last_name:
            user.last_name = last_name

        if name:
            user.name = name
        user.role = Roles.OFFICER
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    jwt_key = models.UUIDField(default=uuid.uuid4)

    objects = BaseUserManager()
    role = models.PositiveSmallIntegerField(
        choices=Roles.choices(), default=Roles.CREWMEMBER
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    ship = models.ForeignKey(
        to=Ship,
        related_name="members",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def set_role(self):
        if self.is_superuser:
            self.role = Roles.OFFICER
        else:
            self.role = Roles.CREWMEMBER
        return self

    def set_name(self):
        if not self.name:
            if all((self.first_name, self.last_name)):
                self.name = f"{self.first_name} {self.last_name}"
            else:
                self.name = f"{self.username}"
        return self

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
