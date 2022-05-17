import django_filters

from applications.account.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ("id", "username", "is_superuser")
